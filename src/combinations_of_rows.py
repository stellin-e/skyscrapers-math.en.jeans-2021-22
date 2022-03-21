from const import *
from city import City
extremes = [
    (1, 4),
    (2, 1),
    (3, 1),
    (3, 2),
    (2, 2),
    (4, 1),
    (1, 2),
    (1, 3),
    (2, 3)
]

city = City([0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0])
c = 0
for i0 in extremes:
    for i1 in extremes:
        for i2 in extremes:
            for i3 in extremes:
                row0 = list(GENERALIZED_CONFIGURATIONS[i0])
                row1 = list(GENERALIZED_CONFIGURATIONS[i1])
                row2 = list(GENERALIZED_CONFIGURATIONS[i2])
                row3 = list(GENERALIZED_CONFIGURATIONS[i3])
                rows = [row0, row1, row2, row3]

                for row in rows:
                    for i in range(len(row)):
                        if len(row[i]) == 1:
                            row[i] = row[0]
                
                city.left = [row0[0], row1[0], row2[0], row3[0]]
                city.right = [row0[1], row1[1], row2[1], row3[1]]

                city.top = INV_GEN_CONF[row[0]]

                city.check_solution(rows)
                c += 1

print(c)

                
    
