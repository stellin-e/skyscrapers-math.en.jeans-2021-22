from src.city import City


unique_city = City([3, 2, 1, 3], [3, 2, 1, 3], [2, 3, 2, 1], [2, 3, 2, 1])
not_unique_city = City([2, 1, 3, 2], [2, 1, 3, 2], [2, 3, 1, 2], [2, 3, 1, 2])

print(
    "\nUNIQUE CITY\n" +
    unique_city.format(unique_city.solve_optimized()),
    "\n\nNOT UNIQUE CITY\n" +
    not_unique_city.format(not_unique_city.solve_optimized())
)

c = City([1, 2, 2, 3], [1, 2, 2, 4], [4, 2, 2, 1], [3, 2, 2, 1])

print(c.format(c.solve_optimized()))