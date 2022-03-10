
# All valid combinations of buildings
# For every extreme return the possible configurations of skyscrapers
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

# For every row, return the extremes
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
    (4, 1): (
        {1}, {2}, {3}, {4}
    ),
    (3, 2): (
        {1, 2}, {2, 3}, {4}, {1, 2, 3}
    ),
    (2, 2): (
        {1, 2, 3}, {1, 2, 4}, {1, 2, 4}, {1, 2, 3}
    ),
    (3, 1): (
        {1, 2}, {1, 3}, {1, 2, 3}, {4}
    ),
    (2, 1): (
        {3}, {1, 2}, {1, 2}, {4}
    ),
    (1, 4): (
        {4}, {3}, {2}, {1}
    ),
    (2, 3): (
        {1, 2, 3}, {4}, {2, 3}, {1, 2}
    ),
    (1, 3): (
        {4}, {1, 2, 3}, {1, 3}, {1, 2}
    ),
    (1, 2): (
        {4}, {1, 2}, {1, 2}, {3}
    ),
}

COMBINATIONS_1_TO_4 = [
    (1, 2, 3, 4), (1, 2, 4, 3), (1, 3, 2, 4), (1, 3, 4, 2), (1, 4, 2, 3), (1, 4, 3, 2), 
    (2, 1, 3, 4), (2, 1, 4, 3), (2, 3, 1, 4), (2, 3, 4, 1), (2, 4, 1, 3), (2, 4, 3, 1), 
    (3, 1, 2, 4), (3, 1, 4, 2), (3, 2, 1, 4), (3, 2, 4, 1), (3, 4, 1, 2), (3, 4, 2, 1), 
    (4, 1, 2, 3), (4, 1, 3, 2), (4, 2, 1, 3), (4, 2, 3, 1), (4, 3, 1, 2), (4, 3, 2, 1)
]

SETS_NAMES = {
    (1, 2): "A",
    (1, 3): "B",
    (1, 2, 3): "C",
    (2, 3): "D",
    (1, 2, 4): "E"
}