from const import *
from pprint import pprint
import copy # Used to make deep copies of nested arrays
import os
from ast import literal_eval

def convert_known_cells_to_int(rows):
    """
    Function used to convert cells with sets of length 1 to
    cells with only the int inside the cell

    Ex.: [{1}, {2}, {3, 4}, {4}] --> [1, 2, {3, 4}, 4]
    """

    for row in rows:
        for x in range(len(row)):
            cell = row[x]
            if type(cell) == set:
                if len(cell) == 1:
                    row[x] = list(cell)[0] # Take the first (and only) element of the set

    return rows

x = [[{1}, {2}, {3, 4}, {4}]]
print(convert_known_cells_to_int(x))


def complete_obvious_cells(rows):
    """
    Function used to complete obvious rows (rows with 3 known values and 1 variable)
    """
    # TODO: Might need fixes, because the variable put in the unknown cell might
    # not match the values that it can take.
    # For ex.: if row == [1, 2, {2, 4}, 4] and the func completes it as [1, 2, 3, 4], 
    # it is wrong

    # Subtract columns
    for y in range(4):
        row = rows[y]
        known_values = set() # Set with the known values of the row
        unknown_value = None

        for cell in row:
            
            if len(cell) == 1:
                # NOTE: .update() updates the set with the union of itself and cell
                known_values.update(cell)
            else:
                unknown_value = cell
        
        if len(known_values) == 3:
            # Find the unknown value in the row and subtract its value
            # with the known values
            unknown_value_index = row.index(unknown_value)                    
            rows[y][unknown_value_index] = unknown_value - known_values

    # Subtract columns
    for x in range(4):
        
        col = [rows[0][x], rows[1][x], rows[2][x], rows[3][x]]

        known_values = set() # Set with the known values of the column
        unknown_value = None

        for cell in col:
            
            if len(cell) == 1:
                # NOTE: .update() updates the set with the union of itself and cell
                known_values.update(cell)
            else:
                unknown_value = cell
        
        if len(known_values) == 3:
            # Find the unknown value in the column and subtract its value
            # with the known values
            unknown_value_index = col.index(unknown_value)                    
            rows[unknown_value_index][x] = unknown_value - known_values
    
    return rows

def has_duplicates(rows):
    """
    Calculates whether there are duplicates on a row or column of a city
    """
    has_dupes = False

    # Subtract columns
    for y in range(4):
        row = rows[y]
        # Set with the unique constant values of the row
        unique_values = set()
        # All the constant value in the row
        all_values = []

        for cell in row:
            if len(cell) == 1:
                unique_values.update(cell)
                all_values.append(cell)
        
        # If the number of unique values in a row is less than the number of the
        # total constant values in a row, there are duplicates
        if len(unique_values) < len(all_values):
            has_dupes = True

        # Subtract columns
    for x in range(4):
        col = [rows[0][x], rows[1][x], rows[2][x], rows[3][x]]
        unique_values = set()
        all_values = []

        for cell in col:
            if len(cell) == 1:
                unique_values.update(cell)
                all_values.append(cell)
        
        if len(unique_values) < len(all_values):
            has_dupes = True

    return has_dupes

def format(top, left, bottom, right, rows):
        invalid = False
        # Strings to append at the end of the output
        append_to_end = []

        if not rows:
            rows = [["x","x","x","x",],["x","x","x","x",],["x","x","x","x",],["x","x","x","x",]]
            invalid = True

        for y in range(len(rows)):
            row = rows[y]
            for x in range(len(row)):
                cell = rows[y][x]
                if type(cell) == set:
                    set_name =  SETS_NAMES[tuple(cell)]
                    rows[y][x] = set_name
                    # String to append at the end of the file to describe the
                    # the sets
                    string = f"{set_name} = {cell}"
                    if string not in append_to_end: 
                        append_to_end.append(string)

        out = f"""┌───┬───┬───┬───┬───┬───┐
│   │ {top[0]} │ {top[1]} │ {top[2]} │ {top[3]} │   │
├───┼───┼───┼───┼───┼───┤
│ {left[0]} │ {rows[0][0]} │ {rows[0][1]} │ {rows[0][2]} │ {rows[0][3]} │ {right[0]} │
├───┼───┼───┼───┼───┼───┤
│ {left[1]} │ {rows[1][0]} │ {rows[1][1]} │ {rows[1][2]} │ {rows[1][3]} │ {right[1]} │
├───┼───┼───┼───┼───┼───┤
│ {left[2]} │ {rows[2][0]} │ {rows[2][1]} │ {rows[2][2]} │ {rows[2][3]} │ {right[2]} │
├───┼───┼───┼───┼───┼───┤
│ {left[3]} │ {rows[3][0]} │ {rows[3][1]} │ {rows[3][2]} │ {rows[3][3]} │ {right[3]} │
├───┼───┼───┼───┼───┼───┤
│   │ {bottom[0]} │ {bottom[1]} │ {bottom[2]} │ {bottom[3]} │   │
└───┴───┴───┴───┴───┴───┘\n"""

        if invalid:
            out += "Invalid city\n"

        for string in append_to_end:
            out += string + "\n"

        return out

def has_unknown_values(rows):
    for y in range(4):
        for x in range(4):
            cell = rows[y][x]
            if type(cell) == set:
                if len(cell) > 1:
                    return True
    return False

def unknown_val_indices(rows):
    """
    Returns position of unknown values as (y, x) tuples
    """
    indices = []
    for y in range(4):
        for x in range(4):
            cell = rows[y][x]
            if len(cell) > 1:
                indices.append((y, x))
    
    return indices

def solve_unique_city(top, left, bottom, right):
    """
    Algorithm to solve unique cities and part of non-unique ones
    """
    try:
        rows = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]

        for y in range(4):
            row = rows[y]
            for x in range(4):
                cell = row[x]

                top_ext = top[x]
                bottom_ext = bottom[x]
                left_ext = left[y]
                right_ext = right[y]

                vertical_values = GENERALIZED_CONFIGURATIONS[(top_ext, bottom_ext)][y]
                horizontal_values = GENERALIZED_CONFIGURATIONS[(left_ext, right_ext)][x]
                
                rows[y][x] = vertical_values.intersection(horizontal_values)

        # Subtract columns
        for y in range(4):
            row = rows[y]
            known_values = set() # Set with the known values of the row
            unknown_value = None

            for cell in row:
                
                if len(cell) == 1:
                    # NOTE: .update() updates the set with the union of itself and cell
                    known_values.update(cell)
                else:
                    unknown_value = cell
            
            if len(known_values) == 3:
                # Find the unknown value in the row and subtract its value
                # with the known values
                unknown_value_index = row.index(unknown_value)                    
                rows[y][unknown_value_index] = unknown_value - known_values

        # Subtract columns
        for x in range(4):
            
            col = [rows[0][x], rows[1][x], rows[2][x], rows[3][x]]

            known_values = set() # Set with the known values of the column
            unknown_value = None

            for cell in col:
                
                if len(cell) == 1:
                    # NOTE: .update() updates the set with the union of itself and cell
                    known_values.update(cell)
                else:
                    unknown_value = cell
            
            if len(known_values) == 3:
                # Find the unknown value in the column and subtract its value
                # with the known values
                unknown_value_index = col.index(unknown_value)                    
                rows[unknown_value_index][x] = unknown_value - known_values

        for y in range(4):
            for x in range(4):
                cell = rows[y][x]
                if len(cell) == 1:
                    rows[y][x] = list(cell)[0]

    except Exception as e:
        return None
    
    return rows

def solve_non_unique_int(rows: list):
    """
    Algorithm used to solve non-unique cities given the inner rows
    """
    solutions = []


    # Find unknown values
    ##print(rows)
    ind = unknown_val_indices(rows)
    #print("ind", ind)

    # This does not work yet
    for y in range(4):
        for x in range(4):
            cell = rows[y][x]
            if type(cell) == int:
                rows[y][x] = {cell}

    RANGE_LIST = [0, 1, 2, 3]

    # Choose first unknown index
    first_cell_pos = ind[0] # Index of first unknown cell
    #print("\nPOSIZIONE", first_cell_pos)
    first_cell_values = rows[first_cell_pos[0]][first_cell_pos[1]] # Get the values of first index
    #print("Possible values", first_cell_values)
    
    # Calculate all solutions for each anchor cells chosen
    for anchor in first_cell_values:
        valid = True
        #print("\nvalue:", anchor)

        sol = copy.deepcopy(rows) # Get deep copy of original rows
        sol[first_cell_pos[0]][first_cell_pos[1]] = {anchor}

        #print("modified sol", sol)

        valid_x = RANGE_LIST.copy()
        valid_x.remove(first_cell_pos[1])
        
        valid_y = RANGE_LIST.copy()
        valid_y.remove(first_cell_pos[0])
        
        #print("valid_x/y", valid_x, valid_y)
        # Subtract rows
        for x in valid_x:
            cell = sol[first_cell_pos[0]][x]
            new_value = cell - {anchor}
            # If an empty set is obtained, the anchor cell is equal to a value on the
            # row, therefore making the cell invalid
            if len(new_value) == 0:
                valid = False
            else:
                cell -= {anchor}

        # Subtract columns
        for y in valid_y:
            cell = sol[y][first_cell_pos[1]]
            new_value = cell - {anchor}
            # If an empty set is obtained, the anchor cell is equal to a value on the
            # row, therefore making the cell invalid
            if len(new_value) == 0:
                valid = False
            else:
                cell -= {anchor}
                
        #pprint(sol)
        #print("valid?", valid)

        if valid == True:
            solutions.append(sol)
    
    new_solutions = []
    # Find equal values on rows/coluymns
    for sol in solutions:
        if not has_duplicates(sol):
            new_solutions.append(sol)

    return new_solutions

def solve_non_unique(top, left, bottom, right):
    """
    Algorithm used to solve non-unique cities given the 4 borders
    """
    try:
        # Solve unique cells
        # This is the base city
        rows = solve_unique_city(top, left, bottom, right)

        # If the city is unique, it's already solved
        if not has_unknown_values(rows):
            return [rows]

        for y in range(4):
            for x in range(4):
                cell = rows[y][x]
                if type(cell) == int:
                    rows[y][x] = {cell}

        # Solve non unique part of the base city
        solutions = []
        
        # TODO: -Clean up and check if always valid
        # First solve
        sol = solve_non_unique_int(rows)
        #pprint(sol)
        #print(len(sol))
        #print()

        for i in sol:
            #print(sol.index(i))
            step2 = solve_non_unique_int(i)
            #pprint(step2)
            #print("\n\n")
            
            # TODO: Is this really the final step?
            for final_step in step2:
                #print("BEFORE")
                #pprint(j)
                #print()
                final_step = complete_obvious_cells(final_step)
                # print("AFTER")
                # pprint(j)
        
                solutions.append(final_step)
        
        return solutions
    
    # TODO: I don't know what exception to use
    except Exception:
        return None

if __name__ == "__main__":
    ext = [[1, 2, 2, 3], [1, 2, 2, 4], [3, 2, 2, 1], [4, 2, 2, 1]]
    x = solve_non_unique(*ext)
    ext = [[2, 4, 1, 2], [2, 1, 3, 2], [2, 1, 4, 2], [2, 3, 1, 2]]
    x1 = solve_non_unique(*ext)

    for i in [x, x1]:
        pprint(i)
        print()
    # print("\nsolutions:")
    # pprint(x)
    # for i in x:
    #     print(format(*ext, i))

def check_solution(top, left, bottom, right, rows: list, return_formatted=False):
    """
        Check if a solution given in rows is valid.
        If all the rows and columns are valid, so they are correspond to the
        costant values, then the whole solution is valid.

        TODO: Cleanup algorithm
    """

    rows = convert_known_cells_to_int(rows)

    valid = False
    valid_lines = 0 # line = row or column

    # Check rows
    for i in range(len(rows)):
        row = tuple(rows[i])
        
        left_cell = left[i]
        right_cell = right[i]
        valid_rows = VALID_CONFIGURATIONS[(left_cell, right_cell)]
        if row in valid_rows:
            valid_lines += 1
    
        # Check columns
    for i in range(len(rows)):
        column = tuple([row[i] for row in rows]) # Take the i-th element of each row to make a column
        top_cell = top[i]
        bottom_cell = bottom[i]
        valid_columns = VALID_CONFIGURATIONS[(top_cell, bottom_cell)]

        if column in valid_columns:
            valid_lines += 1

    if valid_lines == 8:
        valid = True
    
    return valid

def generalize_row(row):
    possible_exts = []

    for ext, gen_row in GEN_CONF_TUPLES.items():
        c = 0
        for tup, gen_tuple in zip(row, gen_row):
            
            for i in tup:
                if i in gen_tuple:    
                    c += 1
                    break
        
        if c == 4:
            possible_exts.append(ext)

    return possible_exts

def find_symmetries(top, left, bottom, right):
    """
    Find all symmetries of a specific set of borders (extremes)
    """
    # NOTE: list[::-1] inverts list
    base = [top, left, bottom, right]
    # Inversions (horizontal, vertical, diagonals)
    inv_horizontal = (top[::-1], right, bottom[::-1], left)
    inv_vertical = (bottom, left[::-1], top, right[::-1])
    inv_left_diagonal = (right[::-1], bottom[::-1], left[::-1], top[::-1])
    inv_right_diagonal = (left, top, right, bottom)
    # Rotations
    rot_90_deg_left = (right, top[::-1], left, bottom[::-1])
    rot_90_deg_right = (left[::-1], bottom, right[::-1], top)
    rot_180_deg = (bottom[::-1], right[::-1], top[::-1], left[::-1])
    
    # Return all the symmetries
    return (
        base,
        inv_horizontal,
        inv_vertical,
        inv_left_diagonal,
        inv_right_diagonal,
        rot_90_deg_left,
        rot_90_deg_right,
        rot_180_deg
    )

extremes = [
    (2, 2),
    (1, 4),
    (2, 1),
    (1, 2),
    (1, 3),
    (2, 3),
    (3, 1),
    (4, 1),
    (3, 2),
]

invalids = []
valids = []
# print(
#     generalize_row(
#         ((1, 2, 4,), (3,), (1, 2), (1, 2, 4))
#     )
# )

flag = True

if not flag:
    quit()

for col1 in extremes:
    for col2 in extremes:
        for col3 in extremes:
            for col4 in extremes:
                columns = [col1, col2, col3, col4]
                # Get top and bottom extremes
                top = [i[0] for i in columns]
                bottom = [i[1] for i in columns]

                inner_rows = [
                    [], 
                    [], 
                    [], 
                    []
                ]

                inner0 = GEN_CONF_TUPLES[(top[0], bottom[0])]
                inner1 = GEN_CONF_TUPLES[(top[1], bottom[1])]
                inner2 = GEN_CONF_TUPLES[(top[2], bottom[2])]
                inner3 = GEN_CONF_TUPLES[(top[3], bottom[3])]

                inners = [inner0, inner1, inner2, inner3]

                for inner in inners:
                    for i, number in zip(range(len(inner_rows)), inner):
                        inner_rows[i].append(number)

                try:
                    # Calculate left and right extremes
                    left = []
                    right = []

                    pos_ext0 = generalize_row(inner_rows[0])
                    pos_ext1 = generalize_row(inner_rows[1])
                    pos_ext2 = generalize_row(inner_rows[2])
                    pos_ext3 = generalize_row(inner_rows[3])
                        
                    for ext0 in pos_ext0:
                        for ext1 in pos_ext1:
                            for ext2 in pos_ext2:
                                for ext3 in pos_ext3:
                                    left = [ext0[0], ext1[0], ext2[0], ext3[0]]
                                    right = [ext0[1], ext1[1], ext2[1], ext3[1]]
                                    
                                    borders = [top, left, bottom, right]
                                    #sol = solve_unique_city(*borders)
                                    solutions = solve_non_unique(*borders)
                                    
                                
                                    if not solutions:
                                        invalids.append(borders)
                                    else:
                                        for sol in solutions:
                                            is_valid = check_solution(*borders, sol)
                                            if is_valid:
                                                valids.append(borders)
                                            else:
                                                invalids.append(borders)

                except KeyError as e:
                    invalids.append([top, bottom])
                    
                    print("\nInvalid\n\n")
                    input()
print(len(invalids), "invalids")
print(len(valids), "valids")

BASE_FOLDER = os.path.dirname(os.path.realpath(__file__))
NON_UNIQUE_VALIDS_PATH = os.path.join(BASE_FOLDER, "results/non-unique-valids.txt")
NON_UN_VAL_NO_SYMM_PATH = os.path.join(BASE_FOLDER, "results/non-unique-valids-no-symm.txt")

print(
    """
1: write all non-unique cities to: non-unique-valids.txt
2: check all and write to: non-unique-valids-no-symm.txt
3: cross check between the two files
"""
    )
action = input("> ")

# TODO: Use JSON for all of this?

if action == "1":
    # TODO: Clean up tuple_Valids
    tuple_valids = []
    for valid in valids:
        tuple_valids.append(tuple([tuple(i) for i in valid]))

    tuple_valids = tuple(tuple_valids)
    with open(NON_UNIQUE_VALIDS_PATH, "w") as f:
        f.write("\n".join([str(i) for i in tuple_valids]))

elif action == "2":
    with open(NON_UNIQUE_VALIDS_PATH, "r") as f:
        lines = f.readlines()
    
    # Evaluate every line (which is a tuple) and turn them to tuples
    valid_cities = [
        literal_eval(line.strip()) for line in lines 
    ]
    # Lookup table for symmetries
    symm_lookup_table = {}
    unique_cities = set()

    # Make lookup table
    for city in valid_cities:
        symmetries = find_symmetries(*city)
        # TODO: Make tuples be the return value of the find_symmetries function
        symmetries = [tuple(s) for s in symmetries]
        print(symmetries)
        for symm in symmetries:
            
            if symm not in symm_lookup_table:
                symm_lookup_table[symm] = symmetries[0] # Every symmetry references the base
                unique_cities.add(city)
    
    print(len(unique_cities))

    with open(NON_UN_VAL_NO_SYMM_PATH, "w") as f:
        f.write("\n".join([str(i) for i in unique_cities]))

# TODO: Fix cross-check
elif action == "3":
    with open(NON_UN_VAL_NO_SYMM_PATH, "r") as f:
        lines = f.readlines()
    unique_cities = [
        literal_eval(line.strip()) for line in lines
    ]

    with open(NON_UNIQUE_VALIDS_PATH, "r") as f:
        lines = f.readlines()
    found_non_unique = [
        literal_eval(line.strip()) for line in lines
    ]

    all_symmetries = []

    for city in unique_cities:
        all_symmetries.extend(find_symmetries(*city))

    for found in found_non_unique:
        if found not in all_symmetries:
            print(found)
            raise Exception("There is a mismatch between the two files, so the algorithm is wrong.")
    
    print("Cross-check completed successfully!")