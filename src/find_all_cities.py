from datetime import datetime, timezone
from const import *
import numpy as np

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

# for i in range(10 ** 8):
#     digits = base_convert(i, 4)
#     solve_city(digits[0:3], digits[4:7], digits[8:11], digits[12:15])
     
extremes = [
    (1, 2),
    (1, 3),
    (1, 4),
    (2, 2),
    (2, 3),

    (2, 1),
    (3, 1),
    (4, 1),
    (3, 2)
]


counter = 0
valids = 0
total = 9**8
start_time = datetime.now(timezone.utc)
try:
    for i in range(12_104_100, total):
        result = np.array([
            1, 1, 1, 
            1, 1, 1, 
            1, 1, 1, 
        ])
        idx = 0
        while i > 0:
            result[idx] = (i % 9) + 1
            i = i // 9
            idx += 1
        
        i = result

        digits = [extremes[i] for i in range(len(i))]

        top = [digits[0][0], digits[1][0], digits[2][0], digits[3][0]]
        bottom = [digits[0][1], digits[1][1], digits[2][1], digits[3][1]]
        left = [digits[4][0], digits[5][0], digits[6][0], digits[7][0]]
        right = [digits[4][1], digits[5][1], digits[6][1], digits[7][1]]

        solution = solve_city(top, left, bottom, right)
        check = check_solution(top, left, bottom, right, solution)

        valids += check # 0: Invalid, 1: Valid
        
        counter += 1

except KeyboardInterrupt:
    pass
finally:
    stop_time = datetime.now(timezone.utc)
    delta = stop_time - start_time
    cities_per_sec = counter/delta.total_seconds()
    eta = total / cities_per_sec


    print(
f"""
{valids:,} valid cities on {counter:,} total.
Time elapsed: {delta}
Cities/s: {round(cities_per_sec, 2)}
ETA: {eta:3f} sec
     {eta/60:.3f} min
     {eta/3600:.3f} h""")  