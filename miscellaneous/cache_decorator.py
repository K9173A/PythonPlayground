import functools
import time


def cache(func):
    cached_data = {}

    @functools.wraps(func)
    def inner(*args, **kwargs):
        print(f'Cached data: {cached_data}')
        if args not in cached_data:
            cached_data[args] = func(*args, **kwargs)
        return cached_data[args]

    return inner


def timing(func):

    @functools.wraps(func)
    def inner(*args, **kwargs):
        start_ts = time.time()
        result = func(*args, **kwargs)
        end_ts = time.time()
        print(f'Function took {end_ts - start_ts} to execute')
        return result

    return inner


@timing
@cache
def sum_up_to(n):
    result = 0
    for i in range(n):
        result += i
        time.sleep(1)
    return result


if __name__ == '__main__':
    for _ in range(20):
        sum_up_to(10)
