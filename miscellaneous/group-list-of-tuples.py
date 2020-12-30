# coding=utf-8
import itertools
import operator

data = [
    (2, 172, 1, 5, False),
    (4, 174, 1, 5, False),
    (156, 173, 1, None, False),
    (152, 171, 1, 6, False),
    (153, 171, 2, 2, False),
    (155, 173, 2, 1, False)
]

# Группировка по второму значению
sorted_data = [
    list(group) for _, group in itertools.groupby(
        sorted(data, key=operator.itemgetter(1)), key=operator.itemgetter(1)
    )
]

for r in sorted_data:
    print(r)
