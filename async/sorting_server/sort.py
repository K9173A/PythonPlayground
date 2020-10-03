"""
Данный модуль предназначен для различных видов сортировок, которые будут
использоваться сервером для эмуляции "долгой операции". Так как сортировки
бывают разные по алгоритмической сложности, то и время выполнения может
варьироваться, что и любопытно протестировать.
"""


def sort(sort_name, collection):
    if sort_name == 'bubble_sort':
        return bubble_sort(collection)
    return []


def bubble_sort(collection):
    """
    Реализация пузырьковой сортировки.
    :param collection: любая изменяемая коллекция с гетерогенными элементами,
    которые можно сравнивать.
    :return: коллекция с элементами, расположенными по возрастанию.
    """
    length = len(collection)
    for i in range(length - 1):
        swapped = False
        for j in range(length - 1 - i):
            if collection[j] > collection[j + 1]:
                swapped = True
                collection[j], collection[j + 1] = collection[j + 1], collection[j]
        if not swapped:
            break
    return collection
