# from timeit import timeit
# from matplotlib import pyplot as plt

# code_1st_algo = """
# from city import City


# city = City([3, 2, 1, 3], [3, 2, 1, 3], [2, 3, 2, 1], [2, 3, 2, 1])
# city.solve_1st()
# """

# code_2nd_algo = """
# from city import City

# city = City([3, 2, 1, 3], [3, 2, 1, 3], [2, 3, 2, 1], [2, 3, 2, 1])
# city.solve_optimized()
# """


# # time_1 = timeit(code_1st_algo, number=100)
# # time_2 = timeit(code_2nd_algo, number=100)
# # all_time_2 = round(time_2 * (2**32), 2)
# # print(f"""
# # solve_1st:          {time_1:.5f} s
# # solve_optimized:    {time_2:.5f} s

# # all cities opt.:    {all_time_2} s
# #                     {all_time_2/60:2f} min
# #                     {all_time_2/3600:2f} h
# #                     {all_time_2/3600/24:2f} d

# # """)



# solve_times = []
# n = 750
# step = 1

# range_ = range(1, n+1, step)

# for i in range_:
#     t = timeit(code_2nd_algo, number=i)
    
#     solve_times.append(t)

# # scale_factor = 5

# # xmin, xmax = plt.xlim()
# # ymin, ymax = plt.ylim()

# # plt.xlim(xmin * scale_factor, xmax * scale_factor)
# # plt.ylim(ymin * scale_factor, ymax * scale_factor)

# plt.plot(list(range_), solve_times)
# plt.xlabel("N. of calculations")
# plt.ylabel("Time [s]")
# plt.show()

#%%

from timeit import timeit

code_1 = """
import numpy as np
sum(range(1_000_000))

"""

code_2 = """
import numpy as np
np.sum(np.arange(0, 1_000_000))
"""

code_1_time = timeit(code_1, number=1)
code_2_time = timeit(code_2, number=1)
print(f"""
numpy:  {code_1_time}
normal: {code_2_time}

""")
# %%
