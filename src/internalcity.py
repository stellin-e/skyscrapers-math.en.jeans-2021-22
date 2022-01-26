from const import *

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


