import functools


def factorial(n):
    if n > 1:
        # Первый параметр - это функция, по которой будут производиться операции с числами.
        # В нашем случае нужно перемножение ряда чисел.
        return functools.reduce(lambda x, y: x * y, [i for i in range(1, n + 1)])
    elif 0 <= n <= 1:
        return 1
    else:
        raise ValueError('Value can not be negative!')


if __name__ == '__main__':
    # Нахождение факториалов: 0! ... 10!
    for j in range(10):
        print(factorial(j))
