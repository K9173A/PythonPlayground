"""
Сложность:
1. Худший случай: O(n^2) - когда нужно расставить элементы по возрастанию,
   а они расположены по убыванию. O(n^2) даёт итерация по 2 циклам: внешний
   цикл (сложность которого равна O(n)) мы умножаем на внутренний (он тоже
   равен O(n)). O(n * n) = O(n^2)
2. Лучший случай: O(n) - когда все элементы расположены по возрастанию.
   Сложность получается из-за того, что имеется переменная swapped,
   которая позволяет прервать алгоритм, если не было осуществлено ни одной
   перестановки за цикл, соответвенно для внутреннего цикла будет O(1), т.к.
   проходимся только один раз, и после swapped=False выходим. Итого:
   O(n) * O(1) = O(n)
3. Средний случай: O(n^2).
"""


def bubble_sort(seq):
    """
    Реализация пузырьковой сортировки.
    :param seq: любая изменяемая коллекция с гетерогенными элементами,
    которые можно сравнивать.
    :return: коллекция с элементами, расположенными по возрастанию.
    Examples:
    >>> bubble_sort([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> bubble_sort([])
    []
    >>> bubble_sort([-2, -5, -45])
    [-45, -5, -2]
    >>> bubble_sort([-23, 0, 6, -4, 34])
    [-23, -4, 0, 6, 34]
    >>> bubble_sort([-23, 0, 6, -4, 34]) == sorted([-23, 0, 6, -4, 34])
    True
    """
    length = len(seq)
    # Сортировка предпологает прохождение по всей коллекции. Внешний цикл
    # занимается как раз итерацией через все элементы. i - это счётчик
    # элементов, которые уже были отсортированы, потому что внутренний цикл
    # за одну проходку сравнивает все соседние числа. Соответственно на
    # каждой итерации будет появляться 1 отсортированный элемент. Он будет
    # перемещён в конец, так как мы сортируем по возрастанию.
    for i in range(length - 1):
        # Данная переменная нужна в качестве флага, который показывает,
        # была ли выполнена на текущем цикле "полезная работа" в виде
        # перестановок элементов или нет. Если перестановки были, значит
        # можно продолжать сортировать, так как ещё остались неотсортиро-
        # ванные элементы,
        swapped = False
        # Внутренний цикл занимается перестановкой элементов. Выражение
        # length - 1 - i вычитает i из length, чтобы ограничить итерацию
        # только на НЕотсортированных элементах. Ведь отсортированные эле-
        # менты не будут больше переставляться! Соответственно в конце
        # коллекции будет набор элементов, зафиксированных в своём положении.
        for j in range(length - 1 - i):
            # Если текущий элемент больше следующего за ним...
            if seq[j] > seq[j + 1]:
                # Перестановка имеется, соответственно текущей цикл не
                # будет последним, будем сортировать дальше.
                swapped = True
                # ... То поменять их местами. БОльшее число сместится ближе к концу.
                seq[j], seq[j + 1] = seq[j + 1], seq[j]
        # Если swapped за текущий цикл перестановок так и не поменяла своё
        # значение на True, то значит мы проитерировались по отсортированным
        # элементам, соответственно сортировать больше нечего. Конец сортировки.
        if not swapped:
            break  # Прикратить итерацию, если коллекция отсортирована
    return seq


if __name__ == '__main__':
    user_input = input('Enter numbers separated by a comma:').strip()
    unsorted = [int(item) for item in user_input.split(',')]
    print(*bubble_sort(unsorted), sep=",")
