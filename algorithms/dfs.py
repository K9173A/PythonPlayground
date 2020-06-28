

def dfs(graph, node):
    """
    Depth-first-search - поиск в глубину в дереве.
    :param graph: граф, который задаётся с помощьюdict, где:
    - ключ - исходный нод.
    - значения - это list с нодами, с которыми связан нод в ключе.
    :param node: нод, с которого начинаем поиск.
    :return:
    """
    # Посещённые ноды
    visited_nodes = []
    # Ноды, которые нужно посетить
    list_of_nodes_to_visit = [node]

    while list_of_nodes_to_visit:
        # one difference from BFS is to pop last element here instead of first one
        current_node = list_of_nodes_to_visit.pop()
        # Если текущий нод не в списке посещённых, то...
        if current_node not in visited_nodes:
            # Добавляем его в список посешённых.
            visited_nodes.append(current_node)
            # Итерируемся через значения (по каждому соседнему ноду)
            for neighbor_node in graph[current_node]:
                # Если нод не списке посещённых, то тдобавляем его в список для посещения.
                if neighbor_node not in visited_nodes:
                    list_of_nodes_to_visit.append(neighbor_node)
    return visited_nodes


if __name__ == '__main__':
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E'],
    }
    print(dfs(graph, 'A'))
