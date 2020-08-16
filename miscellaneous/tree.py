import os


class Tree:
    """
    Выводит содержимое папки в виде дерева.
    """
    MIDDLE_SUBITEM = '├──'
    LAST_SUBITEM = '└──'
    COLOR_BLUE = '\033[94m'
    COLOR_END = '\033[0m'

    def __init__(self, ignore):
        """
        :param ignore: список с элементами, которые нужно игнорировать.
        """
        self.tabs_count = 0
        self.ignore_list = ignore

    def print_content(self, path):
        """
        Печатает в консоли содержимое папки в виде дерева с отступами.
        :param path: путь к нужной папке.
        :return: None.
        """
        print(path)
        self.__traverse_through_path(path)

    def __traverse_through_path(self, path):
        """
        Рекурсивно проходится по пути.
        :param path: путь к папке, дерево которой нужно построить.
        :return: None.
        """
        if not os.path.exists(path):
            raise RuntimeError(f'Path {path} does not exist!')

        content = os.listdir(path)
        for index, entry in enumerate(content):
            current_path = f'{path}/{entry}'

            self.__print_file(entry, index + 1 == len(content))

            if os.path.isdir(current_path) and not self.is_ignored(entry):
                # Для каждой внутренней папки нужно делать на один отступ больше,
                # а при выходе из папки убирать этот отступ.
                self.tabs_count += 1
                self.__traverse_through_path(current_path)
                self.tabs_count -= 1

    def __print_file(self, file, is_last):
        """
        Печатает оттабулированный файл/папку.
        :param file: название файла.
        :param is_last: последний ли элемент в данной папке.
        :return: None.
        """
        symbol = self.LAST_SUBITEM if is_last else self.MIDDLE_SUBITEM
        tabs = '\t' * self.tabs_count
        print(f'{self.COLOR_BLUE}{tabs}{symbol}{self.COLOR_END} {file}')

    def is_ignored(self, entry):
        """
        Определяет, находится ли элементо в списке игнорируемых.
        :param entry: папка или файл.
        :return: bool с результатом проверки.
        """
        return entry in self.ignore_list


def tree(path):
    """
    Просто выводит всё содержимое, рекурсивно проходясь по всем папкам.
    :param path: путь, с которого нужно начинать.
    :return: None.
    """
    if not os.path.exists(path):
        raise RuntimeError(f'Path {path} does not exist!')

    for (current_path, current_path_content, current_path_files) in os.walk(path):
        print(current_path, current_path_content, current_path_files)


if __name__ == '__main__':
    tree = Tree(ignore=['.git'])
    tree.print_content('D:/dev/')
