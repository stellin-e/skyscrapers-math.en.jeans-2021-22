from timeit import timeit

code_1st_algo = """
from city import City


city = City([3, 2, 1, 3], [3, 2, 1, 3], [2, 3, 2, 1], [2, 3, 2, 1])
city.solve_1st()
"""

code_2nd_algo = """
from city import City

city = City([3, 2, 1, 3], [3, 2, 1, 3], [2, 3, 2, 1], [2, 3, 2, 1])
city.solve_optimized()
"""

n = 100
print(
f"""
solve_1st:          {timeit(code_1st_algo, number=n)*1000:.4f} ms
solve_optimized:    {timeit(code_2nd_algo, number=n)*1000:.4f} ms
""")