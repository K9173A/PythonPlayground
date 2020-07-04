

class Graph:
    def __init__(self, graph):
        """
        :param graph: граф, который задаётся с помощью dict, где:
        - ключ - исходный нод.
        - значения - это list с нодами, с которыми связан нод в ключе.
        """
        self.graph = graph

    def search(self, algorithm_name, starting_node_name):
        """
        :param algorithm_name: навание алгоритма. Доступны dfs и bfs.
        :param starting_node_name: нод, с которого начинать алгоритм.
        :return:
        """
        if algorithm_name == 'dfs':
            return self._dfs(starting_node_name)
        if algorithm_name == 'bfs':
            return self._bfs(starting_node_name)
        raise ValueError('Incorrect algorithm name!')

    def _dfs(self, starting_node_name):
        """
        Depth-first-search - поиск в глубину в дереве.
        :param starting_node_name: нод, с которого начинать алгоритм.
        :return: list с последовательностью посещённых нодов.
        """
        # Посещённые ноды
        visited_nodes = []

        # Ноды, которые нужно посетить
        list_of_nodes_to_visit = [starting_node_name]

        # Цикл будет функционировать, пока в списке нодов для посещения
        # не останется ни одного нода.
        while list_of_nodes_to_visit:

            # Вытаскиваем следующий нод из списка нодов, которые нужно посетить
            current_node = list_of_nodes_to_visit.pop(0)

            # Работаем только с не посещёнными нодами.
            if current_node not in visited_nodes:

                # Добавляем его в список посешённых.
                visited_nodes.append(current_node)

                # Соседние ноды
                neighbor_nodes = self.graph[current_node]

                for neighbor_node in neighbor_nodes:
                    # Если нод не списке посещённых, то:
                    if neighbor_node not in visited_nodes:
                        # Добавляем его в список для посещения.
                        list_of_nodes_to_visit.append(neighbor_node)

        return visited_nodes

    def _bfs(self, starting_node_name):
        """
        Breadth-first-search - поиск в ширину в дереве.
        :param starting_node_name: нод, с которого начинать алгоритм.
        :return: list с последовательностью посещённых нодов.
        """
        # Посещённые ноды
        visited_nodes = []

        # Ноды, которые нужно посетить
        list_of_nodes_to_visit = [starting_node_name]

        # Цикл будет функционировать, пока в списке нодов для посещения
        # не останется ни одного нода.
        while list_of_nodes_to_visit:

            # Вытаскиваем следующий нод из списка нодов, которые нужно посетить
            current_node = list_of_nodes_to_visit.pop(0)

            # Соседние ноды
            neighbor_nodes = self.graph[current_node]

            for neighbor_node in neighbor_nodes:
                # Если нод не списке посещённых, то: то добавляем его в список для посещения.
                if neighbor_node not in visited_nodes:
                    # Добавляем его в список посещённых.
                    visited_nodes.append(neighbor_node)
                    # Добавляем его в список для посещения.
                    list_of_nodes_to_visit.append(neighbor_node)

        return visited_nodes


if __name__ == '__main__':
    g = Graph({
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E'],
    })

    print(g.search('dfs', 'A'))
    print(g.search('bfs', 'A'))
