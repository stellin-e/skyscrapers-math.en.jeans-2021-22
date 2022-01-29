from timeit import timeit

code = """
from city import City


city = City([3, 2, 1, 3], [3, 2, 1, 3], [2, 3, 2, 1], [2, 3, 2, 1])
city.solve_1st()
"""

print(f"""
solve_1st: {timeit(code, number=1):.5f}

""")