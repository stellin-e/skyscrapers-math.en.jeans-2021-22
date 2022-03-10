from os import unlink
from typing import List
from pprint import pprint
from const import *

def intersect(iter1, iter2):
    # Intersect two iterables
    return set(tuple(iter1)) & set(iter2)

class City:

    def __init__(self, top: list, left: list, bottom: list, right: list):
        self.top = top
        self.right = right # Right top to bottom
        self.left = left # Left top to bottom
        self.bottom = bottom
        self.rows = []

    def __str__(self) -> str:
        return self.format(self.rows)


    # Very unoptimized algorithm
    def solve_1st(self):

        solution_in_rows = []
        
        #### Insert known values ####
        rows = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]] # Two dimensional 4x4 array
        
        #### Generalize cells ####
        
        # - Generalize rows
        for y in range(4):
            left = self.left[y]
            right = self.right[y]
            generalized_row = GENERALIZED_CONFIGURATIONS[(left, right)]

            for x in range(4):
                rows[y][x] = generalized_row[x]
        
        # - Generalize columns
        for x in range(4):
            top = self.top[x]
            bottom = self.bottom[x]
            generalized_col = GENERALIZED_CONFIGURATIONS[(top, bottom)]
            
            for y in range(4):
                cell = rows[y][x]
                # Intersect the value described by the column with the value described
                # by the row.
                if type(cell) == tuple:
                    new_cell = intersect(cell, generalized_col[y])
                    rows[y][x] = new_cell
                    if len(new_cell) == 1:
                        rows[y][x] = tuple(new_cell)[0]
        
        # - Finish rows
        for y in range(len(rows)):

            row = rows[y]

            known_values = row.copy()
            last_unknown_value_index = None
            
            for i in range(len(row)):
                cell = row[i]

                if type(cell) == set:
                    known_values.remove(cell)
                    last_unknown_value_index = i
            
            if len(known_values) == 3:
                unknown_value = row[last_unknown_value_index]
                # Subtract the set of the unknown value to find the known value.
                # Ex. unknown_value = {1, 2}
                #     known_values = {1, 3, 4}
                #  Then the unkwon value must be 2
                rows[y][last_unknown_value_index] = unknown_value - set(known_values)
    
        for x in range(4):
            for y in range(4):
                cell = rows[y][x]
                if type(cell) == set and len(cell) == 1:
                    rows[y][x] = tuple(cell)[0]

        # Finish columns
        for x in range(len(rows)):
            col = [rows[0][x], rows[1][x], rows[2][x], rows[3][x]]
            
            known_values = col.copy()
            last_unknown_value_index = None

            for i in range(len(col)):
                cell = col[i]

                if type(cell) == set:
                    known_values.remove(cell)
                    last_unknown_value_index = i
            
            if len(known_values) == 3:
                unknown_value = col[last_unknown_value_index]
                rows[last_unknown_value_index][x] = unknown_value - set(known_values)
        
        for x in range(4):
            for y in range(4):
                cell = rows[y][x]
                if type(cell) == set and len(cell) == 1:
                    rows[y][x] = tuple(cell)[0]
        
        if self.check_solution(rows):
            return rows
    
    # More optimized algorithm to solve a city.
    # Gives a solution only when it'
    def solve_optimized(self):
        
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

                    top = self.top[x]
                    bottom = self.bottom[x]
                    left = self.left[y]
                    right = self.right[y]

                    vertical_values = GENERALIZED_CONFIGURATIONS[(top, bottom)][y]
                    horizontal_values = GENERALIZED_CONFIGURATIONS[(left, right)][x]
                    
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
            print(e)
            return
        
        return rows

    def format(self, rows=None):
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
│   │ {self.top[0]} │ {self.top[1]} │ {self.top[2]} │ {self.top[3]} │   │
├───┼───┼───┼───┼───┼───┤
│ {self.left[0]} │ {rows[0][0]} │ {rows[0][1]} │ {rows[0][2]} │ {rows[0][3]} │ {self.right[0]} │
├───┼───┼───┼───┼───┼───┤
│ {self.left[1]} │ {rows[1][0]} │ {rows[1][1]} │ {rows[1][2]} │ {rows[1][3]} │ {self.right[1]} │
├───┼───┼───┼───┼───┼───┤
│ {self.left[2]} │ {rows[2][0]} │ {rows[2][1]} │ {rows[2][2]} │ {rows[2][3]} │ {self.right[2]} │
├───┼───┼───┼───┼───┼───┤
│ {self.left[3]} │ {rows[3][0]} │ {rows[3][1]} │ {rows[3][2]} │ {rows[3][3]} │ {self.right[3]} │
├───┼───┼───┼───┼───┼───┤
│   │ {self.bottom[0]} │ {self.bottom[1]} │ {self.bottom[2]} │ {self.bottom[3]} │   │
└───┴───┴───┴───┴───┴───┘\n"""

        if invalid:
            out += "Invalid city\n"

        for string in append_to_end:
            out += string + "\n"

        return out

    def check_solution(self, rows: list, return_formatted=False):
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
            
            left = self.left[i]
            right = self.right[i]
            valid_rows = VALID_CONFIGURATIONS[(left, right)]
            if row in valid_rows:
                valid_lines += 1
        
        if valid_lines == 4:
            # Check columns
            for i in range(len(rows)):
                column = tuple([row[i] for row in rows]) # Take the i-th element of each row to make a column
                top = self.top[i]
                bottom = self.bottom[i]
                valid_columns = VALID_CONFIGURATIONS[(top, bottom)]

                if column in valid_columns:
                    valid_lines += 1
        else:
            return valid
        
        if valid_lines == 8:
            valid = True
        
        return valid
        
def main():
    city = City([2, 4, 1, 2], [2, 1, 3, 2], [2, 1, 4, 2], [2, 3, 1, 2])
    print(city.format(city.solve_optimized()))



if __name__ == "__main__":
    main()
