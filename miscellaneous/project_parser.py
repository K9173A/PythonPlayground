import functools
import os


class ProjectParser:
    """
    Простой класс, который изначально планировался для реализации парсера проектов.
    По задумке должны были парситься все .py файлы, и выводиться в виде дерева зависимостей.
    """
    def __init__(self, project_root):
        """
        :param project_root: корневая директория, откуда нужно начинать парсинг.
        """
        self.project_root = project_root.rstrip(os.sep)
        self.ignores = ('.git', 'venv', '__pycache__', '.idea', 'site-packages')
        self.tree = {}
        self.modules_paths = None

    def run(self):
        """
        Составляет дерево каталогов и парсит файлы.
        :return: None.
        """
        self.__build_project_tree()
        self.modules_paths = self.__compose_files_list_from_tree(self.tree)
        self.__parse(os.path.join('\\'.join(self.project_root.split(os.sep)[:-1]), self.modules_paths[0]))

    def __parse(self, module_path):
        """
        Выводит содержимое модуля в консоль.
        :param module_path: путь к модулю.
        :return: None.
        """
        with open(module_path, mode='r', encoding='utf-8') as f:
            for line in f.readlines():
                print(line)

    def __compose_files_list_from_tree(self, tree):
        """
        Составляет список путей к файлам, которые были указаны в дереве, собранном
        в методе `__build_project_tree`.
        :param tree: Дерево каталогов.
        :return: список из файлов для дерева каталогов `tree`.
        """
        paths = []
        for parent, content in tree.items():
            # Если у текущей директории имеется поддиректория, то делаем рекурсию
            if isinstance(content, dict):
                for path in self.__compose_files_list_from_tree(content):
                    paths.append(os.path.join(parent, path))
            else:
                paths.append(parent)
        return paths

    def __build_project_tree(self):
        """
        Составляет дереко каталогов. Представляет из себя `dict`, где ключ - это
        название текущией директории, а значение либо `None` - если дочерних папок
        или файлов не было найдено, либо ещё один `dict`, с рекурсивной структурой.
        :return: None.
        """
        rightmost_sep_index = self.project_root.rfind(os.sep)

        for current_path, _, child_files in os.walk(self.project_root):
            project_folders = current_path[rightmost_sep_index + 1:].split(os.sep)

            if self.__is_ignored_directory(project_folders):
                continue

            parent = functools.reduce(dict.get, project_folders[:-1], self.tree)
            parent[project_folders[-1]] = dict.fromkeys(self.__get_filtered_files(child_files))

    def __get_filtered_files(self, files):
        """
        Отфильтровывать только питоновские модули.
        :param files: список с названиями файлов.
        :return: список с питоновскими модулями.
        """
        return [file for file in files if file.endswith('.py')]

    def __is_ignored_directory(self, directories):
        """
        Проверяет, является ли директория игнорируемой.
        :param directories: путь к файлу. Передаётся как список из дерева директорий.
        :return: булевой результат проверки.
        """
        for directory in directories:
            if directory in self.ignores:
                return True
        return False


if __name__ == '__main__':
    pp = ProjectParser('D:\\dev\\PythonPlayground')
    pp.run()
