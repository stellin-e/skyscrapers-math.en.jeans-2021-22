from typing import List
from pprint import pprint
from const import *

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
        
        # TODO: Scrivere un vero algoritmo che risolva, adesso
        # mette semplicemente delle righe

        # Algoritmo 1-4, 2-1, ...
        rows = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]] # Two dimensional 4x4 array
        columns = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        
        ######### Solve columns ##############
        for i in range(4):
            top = self.top[i]
            bottom = self.bottom[i]
            extremes = (top, bottom)

            # 1 at the top, 4 at the bottom
            if extremes == (1, 4):
                rows[0][i] = 4
                rows[1][i] = 3
                rows[2][i] = 2
                rows[3][i] = 1
                
            # 4 at the top, 1 at the bottom
            elif extremes == (4, 1):
                rows[0][i] = 1
                rows[1][i] = 2
                rows[2][i] = 3
                rows[3][i] = 4
            
            # 2 at the top, 1 at the bottom
            elif extremes == (2, 1):
                rows[0][i] = 3
                rows[3][i] = 4
            
            # 1 at the top, 2 at the bottom
            elif extremes == (1, 2):
                rows[0][i] = 4
                rows[3][i] = 3

            # 3 at the top, 2 at the bottom
            elif extremes == (3, 2):
                # The third element from the top is always a 4
                rows[2][i] = 4 
            
            # 2 at the top, 3 at the bottom
            elif extremes == (2, 3):
                # The third element from the bottom (second from the top) is always a 4
                rows[1][i] = 4

            # 1 at the top, 3 at the bottom
            elif extremes == (1, 3):
                rows[0][i] = 4
            
            # 3 at the top, 1 at the bottom
            elif extremes == (3, 1):
                rows[3][i] = 4

        ########## Solve rows #################
        for i in range(4):
            left = self.left[i]
            right = self.right[i]
            extremes = (left, right)

             # 1 at the left, 4 at the right
            if extremes == (1, 4):
                rows[i][0] = 4
                rows[i][1] = 3
                rows[i][2] = 2
                rows[i][3] = 1
            
             # 4 at the left, 1 at the right
            elif extremes == (4, 1):
                rows[i][0] = 1
                rows[i][1] = 2
                rows[i][2] = 3
                rows[i][3] = 4
            
            # 2 at the left, 1 at the right
            elif extremes == (2, 1):
                rows[i][0] = 3
                rows[i][3] = 4
            
            # 1 at the left, 2 at the right
            elif extremes == (1, 2):
                rows[i][0] = 4
                rows[i][3] = 3

            # 3 at the left, 2 at the right
            elif extremes == (3, 2):
                # The third element from the left is always a 4
                rows[i][2] = 4 
            
            # 2 at the left, 3 at the right
            elif extremes == (2, 3):
                # The third element from the right (second from the left) is always a 4
                rows[i][1] = 4
            
            # 1 at the left, 3 at the right
            elif extremes == (1, 3):
                rows[i][0] = 4
            
            # 3 at the left, 1 at the right
            elif extremes == (3, 1):
                rows[i][3] = 4

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
        """
        valid = False
        lines_correct = 0 # line = row or column

        # Check rows
        for i in range(len(rows)):
            row = tuple(rows[i])
            
            left = self.left[i]
            right = self.right[i]
            valid_rows = VALID_CONFIGURATIONS[(left, right)]
            if row in valid_rows:
                lines_correct += 1
        
        if lines_correct == 4:
            # Check columns
            for i in range(len(rows)):
                column = tuple([row[i] for row in rows]) # Take the i-th element of each row to make a column
                top = self.top[i]
                bottom = self.bottom[i]
                valid_columns = VALID_CONFIGURATIONS[(top, bottom)]

                if column in valid_columns:
                    lines_correct += 1
        else:
            return valid
        
        if lines_correct == 8:
            valid = True
        
        if return_formatted == False:
            return valid
        else:
            return self.format(rows)
        
def main():
    city = City([2, 1, 2, 3], [3, 1, 2, 1], [3, 1, 2, 1], [2, 1, 2, 3])
    print(city)

if __name__ == "__main__":
    main()
