from typing import List
from pprint import pprint
print(4**16, "combinazioni totali")

# All valid combinations of buildings
VALID_CONFIGURATIONS = {
    #(left, right)
    (4, 1): ((1, 2, 3, 4),), # In order
    (3, 2): ((1, 2, 4, 3), (1, 3, 4, 2), (2, 3, 4, 1)), # Always a 4 on the 3rd element
    (2, 2): (
        (1, 4, 2, 3), (2, 1, 4, 3), (2, 4, 1, 3), # 3 on the right
        (3, 2, 4, 1), (3, 4, 1, 2), (3, 1, 4, 2) #3 on the left
    ),
    (3, 1): ((2, 1, 3, 4), (2, 3, 1, 4), (1, 3, 2, 4)), # 2 never on 2nd element
    (2, 1): ((3, 1, 2, 4), (3, 2, 1, 4)), # It's always 3, x, y, 4
    
    # (right, left) (Inverted)
    (1, 4): ((4, 3, 2, 1),),
    (2, 3): ((3, 4, 2, 1), (2, 4, 3, 1), (1, 4, 3, 2)),
    (1, 3): ((4, 3, 1, 2), (4, 1, 3, 2), (4, 2, 3, 1)),
    (1, 2): ((4, 2, 1, 3), (4, 1, 2, 3)),
}

INVERSE_VC = {
    (1, 2, 3, 4): (4, 1),
    (1, 2, 4, 3): (3, 2),
    (1, 3, 4, 2): (3, 2),
    (2, 3, 4, 1): (3, 2),
    (1, 4, 2, 3): (2, 2),
    (2, 1, 4, 3): (2, 2),
    (2, 4, 1, 3): (2, 2),
    (3, 2, 4, 1): (2, 2),
    (3, 4, 1, 2): (2, 2),
    (3, 1, 4, 2): (2, 2),
    (2, 1, 3, 4): (3, 1),
    (2, 3, 1, 4): (3, 1),
    (1, 3, 2, 4): (3, 1),
    (3, 1, 2, 4): (2, 1),
    (3, 2, 1, 4): (2, 1),
    (4, 3, 2, 1): (1, 4),
    (3, 4, 2, 1): (2, 3),
    (2, 4, 3, 1): (2, 3),
    (1, 4, 3, 2): (2, 3),
    (4, 3, 1, 2): (1, 3),
    (4, 1, 3, 2): (1, 3),
    (4, 2, 3, 1): (1, 3),
    (4, 2, 1, 3): (1, 2),
    (4, 1, 2, 3): (1, 2)
}

counter = 0 # DEBUG

# All the possible configurations of numbers per cell
GENERALIZED_CONFIGURATIONS = {
    # Left to right
    (4, 1): (
        (1,), (2,), (3,), (4,)
    ),
    (3, 2): (
        (1, 2), (2, 3), (4,), (1, 2, 3)
    ),
    (2, 2): (
        (1, 2, 3), (1, 2, 4), (1, 2, 4), (1, 2, 3)
    ),
    (3, 1): (
        (1, 2), (1, 3), (1, 2, 3), (4,)
    ),
    (2, 1): (
        (3,), (1, 2), (1, 2), (4,)
    ),
    # Right to left
    (1, 4): (
        (4,), (3,), (2,), (1,)
    ),
    (2, 3): (
        (1, 2, 3), (4,), (2, 3), (1, 2)
    ),
    (1, 3): (
        (4,), (1, 2, 3), (1, 3), (1, 2)
    ),
    (1, 2): (
        (4,), (1, 2), (1, 2), (3,)
    )
}

COMBINATIONS_1_TO_4 = [
    (1, 2, 3, 4), (1, 2, 4, 3), (1, 3, 2, 4), (1, 3, 4, 2), (1, 4, 2, 3), (1, 4, 3, 2), 
    (2, 1, 3, 4), (2, 1, 4, 3), (2, 3, 1, 4), (2, 3, 4, 1), (2, 4, 1, 3), (2, 4, 3, 1), 
    (3, 1, 2, 4), (3, 1, 4, 2), (3, 2, 1, 4), (3, 2, 4, 1), (3, 4, 1, 2), (3, 4, 2, 1), 
    (4, 1, 2, 3), (4, 1, 3, 2), (4, 2, 1, 3), (4, 2, 3, 1), (4, 3, 1, 2), (4, 3, 2, 1)
]

class City:

    def __init__(self, top: list, left: list, bottom: list, right: list):
        self.top = top
        self.right = right # Right top to bottom
        self.left = left # Left top to bottom
        self.bottom = bottom
    
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
        if rows == None:
            rows = [["x","x","x","x",],["x","x","x","x",],["x","x","x","x",],["x","x","x","x",]]
        
        out = f"  _{self.top[0]}_{self.top[1]}_{self.top[2]}_{self.top[3]}_\n"\
              f"{self.left[0]}| {rows[0][0]} {rows[0][1]} {rows[0][2]} {rows[0][3]} |{self.right[0]}\n"\
              f"{self.left[1]}| {rows[1][0]} {rows[1][1]} {rows[1][2]} {rows[1][3]} |{self.right[1]}\n"\
              f"{self.left[2]}| {rows[2][0]} {rows[2][1]} {rows[2][2]} {rows[2][3]} |{self.right[2]}\n"\
              f"{self.left[3]}| {rows[3][0]} {rows[3][1]} {rows[3][2]} {rows[3][3]} |{self.right[3]}\n"\
              f" --{self.bottom[0]}-{self.bottom[1]}-{self.bottom[2]}-{self.bottom[3]}--"

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

class InternalCity:

    def __init__(self):
        self.top = [0, 0, 0, 0]
        self.left = [0, 0, 0, 0]
        self.bottom = [0, 0, 0, 0]
        self.right = [0, 0, 0, 0]
        self.rows = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]
    
    def find_sides(self):
        # Rows
        for i in range(len(self.rows)):
            row = tuple(self.rows[i])
            extremes = INVERSE_VC[row]
            self.left[i] = extremes[0]
            self.right[i] = extremes[1]

        # Columns
        for i in range(len(self.rows)):
            column = tuple([row[i] for row in self.rows])
            extremes = INVERSE_VC[column]
            self.bottom[i] = extremes[0]
            self.top[i] = extremes[1]
        
        print(self.format())

        if (
            (self.top == self.right and self.bottom == self.left) or
            (self.top == self.left and self.bottom == self.right)
        ):
            global counter
            counter += 1

    def find_all_diagonal(self):

        for combination in COMBINATIONS_1_TO_4:

            # Method without for loop
            self.rows[0][0] = combination[0]

            self.rows[0][1] = combination[1]
            self.rows[1][0] = combination[1]

            self.rows[0][2] = combination[2]
            self.rows[1][1] = combination[2]
            self.rows[2][0] = combination[2]

            self.rows[0][3] = combination[3]
            self.rows[1][2] = combination[3]
            self.rows[2][1] = combination[3]
            self.rows[3][0] = combination[3]

            self.rows[1][3] = combination[0]
            self.rows[2][2] = combination[0]
            self.rows[3][1] = combination[0]

            self.rows[2][3] = combination[1]
            self.rows[3][2] = combination[1]
            
            self.rows[3][3] = combination[2]

            print(self.format())
            self.find_sides()

    def find_all_solutions_for_pattern(self, pattern):
        """
        Finds all solutions given a pattern expressed in rows of indices
        that refer to COMBINATIONS_1_TO_4, that the numbers follow.
        Example:
        ```
        pattern = [
            [0, 1, 2, 3],
            [1, 2, 3, 0],
            [2, 3, 0, 1],
            [3, 0, 1, 2]
        ] # All equal indices (0, 1, 2, 3) correspond to equal numbers
        
        # so the inside of a city could be like
        city = [
            [1, 2, 3, 4],
            [2, 3, 4, 1],
            [3, 4, 1, 2],
            [4, 1, 2, 3]
        ]

        print(
            InternalCity().find_all_solutions_for_pattern(pattern)
        )
        ```
        """
        # for pattern_row, city_y in zip(pattern, self.rows):
        #     for pattern_index, city_x in zip(pattern_row, city_y):
        #         self.rows[city_y][city_x] = pattern_index

        # For every row
        for combination in COMBINATIONS_1_TO_4:
            for row_number in range(4):

                row = self.rows[row_number]
                pattern_row = pattern[row_number]

                for i in range(4):
                    combination_index = pattern_row[i]
                    self.rows[row_number][i] = combination[combination_index]

            print(self.format())

    def format(self):
        rows = self.rows
        if rows == None:
            rows = [["x","x","x","x",],["x","x","x","x",],["x","x","x","x",],["x","x","x","x",]]
        
        out = f"  _{self.top[0]}_{self.top[1]}_{self.top[2]}_{self.top[3]}_\n"\
              f"{self.left[0]}| {rows[0][0]} {rows[0][1]} {rows[0][2]} {rows[0][3]} |{self.right[0]}\n"\
              f"{self.left[1]}| {rows[1][0]} {rows[1][1]} {rows[1][2]} {rows[1][3]} |{self.right[1]}\n"\
              f"{self.left[2]}| {rows[2][0]} {rows[2][1]} {rows[2][2]} {rows[2][3]} |{self.right[2]}\n"\
              f"{self.left[3]}| {rows[3][0]} {rows[3][1]} {rows[3][2]} {rows[3][3]} |{self.right[3]}\n"\
              f" --{self.bottom[0]}-{self.bottom[1]}-{self.bottom[2]}-{self.bottom[3]}--"

        return out




# def format_pattern(pattern):

#     for y in pattern:
#         for x in y:
#             if x is None:
#                 x = "-" # Actually call the array index and not this stupid thing


#     out = f"""
# +---------+    
# | {} {} {} {} |
# | {} {} {} {}  |  
# | {} {} {} {}  |  
# | {} {} {} {}  |  
# +---------+
#     """


# def find_all_patterns():
#     pattern = [
#         [None, None, None, None],
#         [None, None, None, None],
#         [None, None, None, None],
#         [None, None, None, None]
#     ]

#     for y in range(len(pattern)):
        
#         row = pattern[y]
#         for x in range(len(row)):
#             pattern = [
#                 [None, None, None, None],
#                 [None, None, None, None],
#                 [None, None, None, None],
#                 [None, None, None, None]
#             ]

            
#             x_number = row[x]
#             pattern[y][x] = 0
        
#             print(pattern[0])
#             print(pattern[1])
#             print(pattern[2])
#             print(pattern[3])
#             print()
        
        
def main():
    pass

if __name__ == "__main__":
    main()
