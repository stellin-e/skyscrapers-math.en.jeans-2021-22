from datetime import datetime, timezone
from re import I
from const import *
import numpy as np
from pprint import pprint

def solve_city(top, left, bottom, right):
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

def solve_non_unique(rows, top, left, bottom, right):
    solutions = []
    try:

        is_unique = True
        pos_of_sets = []

        for y in range(4):
            for x in range(4):
                c = rows[y][x]

                if type(c) == set:
                    is_unique = False
                    pos_of_sets.append((x, y))

        pos_first_set = pos_of_sets[0]
        print(rows)
        first_row = rows[pos_first_set[1]][pos_first_set[0]]
        for v in list(first_row):
            rows[pos_first_set[1]][pos_first_set[0]] = v
            
            # Calculate rows
            # TODO: FIX ALGO
            for y in range(4):
                col = rows[y]
                known_values = set()
                unknown_value = None

                for cell in col:
                    if type(cell) == int:
                        known_values.update({cell})
                    else:
                        unknown_value = cell
                
                if len(known_values) == 3:
                    unknown_value_index = col.index(unknown_value)
                    rows[y][unknown_value_index] = unknown_value - known_values
            
            for x in range(4):
                col = rows[x]
                known_values = set()
                unknown_value = None

                for cell in col:
                    if type(cell) == int:
                        known_values.update({cell})
                    else:
                        unknown_value = cell
                
                if len(known_values) == 3:
                    unknown_value_index = col.index(unknown_value)
                    rows[y][unknown_value_index] = unknown_value - known_values
                        
                    



            # # Subtract columns
            # for y in range(4):
            #     row = rows[y]
            #     known_values = set() # Set with the known values of the row
            #     unknown_value = None

            #     for c in row:
                    
            #         if len(c) == 1 or type(c) == int:
            #             # NOTE: .update() updates the set with the union of itself and cell
            #             known_values.update(c)
            #         else:
            #             unknown_value = c
                
            #     if len(known_values) == 3:
            #         # Find the unknown value in the row and subtract its value
            #         # with the known values
            #         unknown_value_index = row.index(unknown_value)
            #         rows[y][unknown_value_index] = unknown_value - known_values

            # for x in range(4):
                
            #     col = [rows[0][x], rows[1][x], rows[2][x], rows[3][x]]

            #     known_values = set() # Set with the known values of the column
            #     unknown_value = None

            #     for c in col:
                    
            #         if len(c) == 1 or type(c) == int:
            #             # NOTE: .update() updates the set with the union of itself and cell
            #             known_values.update(c)
            #         else:
            #             unknown_value = c
                
            #     if len(known_values) == 3:
            #         # Find the unknown value in the column and subtract its value
            #         # with the known values
            #         unknown_value_index = col.index(unknown_value)
            #         rows[unknown_value_index][x] = unknown_value - known_values

            print(rows)


        # If the city is unique, return the city
        if is_unique:
            return rows
    
    except Exception as e:
        raise e

    return solutions

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

x = solve_city([1, 2, 2, 4], [1, 2, 2, 4], [4, 2, 2, 1], [4, 2, 2, 1])
solve_non_unique(x, [1, 2, 2, 4], [1, 2, 2, 4], [4, 2, 2, 1], [4, 2, 2, 1])
    
# extremes = [
#     (2, 2),

#     (1, 4),
#     (4, 1),

#     (2, 1),
#     (1, 2),

#     (1, 3),
#     (3, 1),

#     (2, 3),
#     (3, 2)
# ]

# invalids = []
# valids = []
# print(
#     generalize_row(
#         ((1, 2, 4,), (3,), (1, 2), (1, 2, 4))
#     )
# )


# for col1 in extremes:
#     for col2 in extremes:
#         for col3 in extremes:
#             for col4 in extremes:
#                 columns = [col1, col2, col3, col4]
#                 # Get top and bottom extremes
#                 top = [i[0] for i in columns]
#                 bottom = [i[1] for i in columns]

#                 inner_rows = [
#                     [], 
#                     [], 
#                     [], 
#                     []
#                 ]

#                 inner0 = GEN_CONF_TUPLES[(top[0], bottom[0])]
#                 inner1 = GEN_CONF_TUPLES[(top[1], bottom[1])]
#                 inner2 = GEN_CONF_TUPLES[(top[2], bottom[2])]
#                 inner3 = GEN_CONF_TUPLES[(top[3], bottom[3])]

#                 inners = [inner0, inner1, inner2, inner3]

#                 for inner in inners:
#                     for i, number in zip(range(len(inner_rows)), inner):
#                         inner_rows[i].append(number)

#                 try:
#                     # Calculate left and right extremes
#                     left = []
#                     right = []

#                     pos_ext0 = generalize_row(inner_rows[0])
#                     pos_ext1 = generalize_row(inner_rows[1])
#                     pos_ext2 = generalize_row(inner_rows[2])
#                     pos_ext3 = generalize_row(inner_rows[3])
                        
#                     for ext0 in pos_ext0:
#                         for ext1 in pos_ext1:
#                             for ext2 in pos_ext2:
#                                 for ext3 in pos_ext3:
#                                     left = [ext0[0], ext1[0], ext2[0], ext3[0]]
#                                     right = [ext0[1], ext1[1], ext2[1], ext3[1]]
                                    
#                                     borders = [top, left, bottom, right]
#                                     sol = solve_city(*borders)
                                    
#                                     if sol is None:
#                                         invalids.append(borders)
#                                     else:
#                                         is_valid = check_solution(*borders, sol)
#                                         if is_valid:
#                                             valids.append(borders)
#                                         else:
#                                             invalids.append(borders)

#                 except KeyError as e:
#                     invalids.append([top, bottom])
                    
#                     print("\nInvalid\n\n")
#                     input()

# print(len(invalids))
# with open("./results/invalids.txt", "w") as f:
#     f.write("\n".join([str(i) for i in invalids]))

# with open("./results/unique-valids.txt", "w") as f:
#     f.write("\n".join([str(i) for i in valids]))

