from timeit import timeit

code_1st_algo = """
from city import City


city = City([2, 1, 3, 2], [2, 1, 3, 2], [2, 3, 1, 2], [2, 3, 1, 2])
city.solve_1st()
"""

code_2nd_algo = """
from city import City

city = City([2, 1, 3, 2], [2, 1, 3, 2], [2, 3, 1, 2], [2, 3, 1, 2])
city.solve_optimized()
"""


print(f"""
solve_1st:          {timeit(code_1st_algo, number=100):.5f}
solve_optimized:    {timeit(code_2nd_algo, number=100):.5f}
""")