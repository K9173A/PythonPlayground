# Python 3.8
import functools
import timeit


class Storage:
    def __init__(self):
        self.number = 500

    @functools.cached_property
    def boardwalk(self):
        # Значение будет всегда одним и тем же, плюс мы не переплачиваем по
        # времени выполнения так как используется кэшированное значение.
        self.number += 1
        return self.number


if __name__ == '__main__':
    s = Storage()
    for _ in range(10):
        start = timeit.default_timer()
        print(s.number)
        end = timeit.default_timer()
        print('time:', end - start)
