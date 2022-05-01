from datetime import datetime, timezone

from cv2 import FlannBasedMatcher
from const import *
import numpy as np
from pprint import pprint
import json
import copy

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
                return True
    return False

# Return position of value as (y, x) tuple
def unknown_val_indices(rows):
    indices = []
    for y in range(4):
        for x in range(4):
            cell = rows[y][x]
            if type(cell) == set:
                indices.append((y, x))
    
    return indices

def solve_unique_city(top, left, bottom, right):
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

def solve_non_unique(top, left, bottom, right):
    solutions = []
    rows = solve_unique_city(top, left, bottom, right)
    is_non_unique = has_unknown_values(rows)
    print("\ninitial", rows)
    print("non-unique?", is_non_unique)
    print()

    # If the city is unique, it's already solved
    if is_non_unique == False:
        print("Does not have unknown values")
        return rows

    # Find unknown values
    print(rows)
    ind = unknown_val_indices(rows)
    print("ind", ind)

    # This does not work yet
    for y in range(4):
        for x in range(4):
            cell = rows[y][x]
            if type(cell) == int:
                rows[y][x] = {cell}

    # TODO: Make this looped

    RANGE_LIST = [0, 1, 2, 3]

    while len(ind) > 0:
        
        # Choose first unknown index
        first_cell_pos = ind[0] # Index of first unknown cell
        print("\nPOSIZIONE", first_cell_pos)
        first_cell_values = rows[first_cell_pos[0]][first_cell_pos[1]] # Get the values of first index
        print("Possible values", first_cell_values)
        
        # Calculate all solutions for each anchor cells chosen
        for anchor in first_cell_values:
            valid = True
            print("\nvalue:", anchor)

            sol = copy.deepcopy(rows) # Get deep copy of original rows
            sol[first_cell_pos[0]][first_cell_pos[1]] = {anchor}

            print("modified sol", sol)

            valid_x = RANGE_LIST.copy()
            valid_x.remove(first_cell_pos[1])
            
            valid_y = RANGE_LIST.copy()
            valid_y.remove(first_cell_pos[0])
            
            print("valid_x/y", valid_x, valid_y)
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
                    
            pprint(sol)
            print("valid?", valid)

            if valid == True:
                solutions.append(sol)
    
        for sol in solutions:
            

    return solutions

if __name__ == "__main__":
    ext = [[1, 2, 2, 3], [1, 2, 2, 4], [3, 2, 2, 1], [4, 2, 2, 1]]
    x = solve_non_unique(*ext)
    print("\nsolutions:")
    pprint(x)
    # for i in x:
    #     print(format(*ext, i))

def check_solution(top, left, bottom, right, rows: list, return_formatted=False):
    """
        Check if a solution given in rows is valid.
        If all the rows and columns are valid, so they are correspond to the
        costant values, then the whole solution is valid.

        TODO: Cleanup algorithm
    """
    
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
    
extremes = [
    (2, 2),
    (1, 4),
    (2, 1),
    (1, 2),
    (1, 3),
    (2, 3),
    (3, 1),
    (4, 1),
    (3, 2)
]

invalids = []
valids = []
# print(
#     generalize_row(
#         ((1, 2, 4,), (3,), (1, 2), (1, 2, 4))
#     )
# )

flag = False

if flag:
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
                                        sol = solve_unique_city(*borders)
                                        
                                        if sol is None:
                                            invalids.append(borders)
                                        else:
                                            is_valid = check_solution(*borders, sol)
                                            if is_valid:
                                                valids.append(borders)
                                            else:
                                                invalids.append(borders)

                    except KeyError as e:
                        invalids.append([top, bottom])
                        
                        print("\nInvalid\n\n")
                        input()

    print(len(invalids))
    with open("./results/invalids.txt", "w") as f:
        f.write("\n".join([str(i) for i in invalids]))

    with open("./results/unique-valids.txt", "w") as f:
        f.write("\n".join([str(i) for i in valids]))