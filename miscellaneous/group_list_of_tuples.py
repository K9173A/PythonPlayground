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
    
# Вот этот вариант точно был протестирован на Python2
data2 = [
    {'id': 1, 'name': 'Andrew'},
    {'id': 1, 'name': 'Mike'},
    {'id': 3, 'name': 'John'},
    {'id': 2, 'name': 'Kyle'},
    {'id': 1, 'name': 'Albert'},
    {'id': 3, 'name': 'Kate'}
]

sorted_data2 = [list(g) for k, g in groupby(v, lambda s: s['id'])]

print(sorted_data2)

