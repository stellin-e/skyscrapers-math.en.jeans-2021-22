import src.city as gr


int_city = gr.InternalCity()

# int_city.find_all_diagonal()
# print(gr.counter, "/ 24 hanno i numeri con le diagonali belle")


pattern = [
    [0, 1, 2, 3],
    [1, 2, 3, 0],
    [2, 3, 0, 1],
    [3, 0, 1, 2]
]
# The question is what are all the valid patterns?


int_city.find_all_solutions_for_pattern(pattern)
print(
    int_city.rows
)

#gr.find_all_patterns()




# # Symmetric on diagonal city ( where two nearby sides are equivalent)
# c1 = gr.City(
#     [2, 1, 2, 2], # top
#     [2, 1, 2, 2], # left
#     [3, 4, 1, 2], # bottom
#     [3, 4, 1, 2]  # right
# )

# print(
#     c1.format(
#         c1.solve_1st()
#     )
# )

# c2 = gr.City(
#     [3, 2, 1, 3],
#     [3, 2, 1, 3],
#     [2, 3, 2, 1],
#     [2, 3, 2, 1]
# )

# print(
#     c2.format(
#         c2.solve_1st()
#     )
# )