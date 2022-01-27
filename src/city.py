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

    # 1st algorithm
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
                print(i, row)
                cell = row[i]

                if type(cell) == set:
                    print(i)
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
                if type(cell) == set:
                    if len(cell) == 1:
                        rows[y][x] = tuple(cell)[0]

        # ######### I don't know ###############
        # if self.check_solution(rows) == False:
        #     if (
        #         self.top == self.left and self.bottom == self.right
        #         or self.top == self.right and self.bottom == self.left
        #     ):
        #         possible_combinations = []
        #         for i in range(len(rows)):
        #             row = rows[i]
        #             left = self.left[i]
        #             right = self.right[i]
        #             extremes = (left, right)

        #             four_index = row.index(4)
        #             set_of_combinations = []
        #             for combination in VALID_CONFIGURATIONS[extremes]:
        #                 if combination.index(4) == four_index:
        #                     set_of_combinations.append(combination)

        #             possible_combinations.append(set_of_combinations)
                
        #         print(possible_combinations)

        #         # Stupid algorithm
        #         for i in range(3):
        #             for j in range(len(rows)):
        #                 rows[j] = possible_combinations[j][i]
                    
        #             if self.check_solution(rows) == True:
        #                 break

        #         print(self.format(rows))


        return rows

    def format(self, rows=None):
        if not rows:
            rows = [["x","x","x","x",],["x","x","x","x",],["x","x","x","x",],["x","x","x","x",]]
        
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
└───┴───┴───┴───┴───┴───┘"""

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
    city = City([3, 2, 1, 3], [3, 2, 1, 3], [2, 3, 2, 1], [2, 3, 2, 1])
    print(city.format(city.solve_1st()))

if __name__ == "__main__":
    main()
