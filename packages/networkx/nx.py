import networkx as nx
import matplotlib.pyplot as plt


graph = nx.Graph()

# Добавление вершин графа
graph.add_weighted_edges_from([
    ('a', 'b', 0.9),
    ('b', 'c', 0.5),
    ('a', 'c', 0.5),
    ('c', 'd', 1.2)
])

# Алгоритм Дейкстры (кротчайший маршрут от `a` до `d`).
print(nx.dijkstra_path(graph, 'a', 'd'))  # ['a', 'c', 'd']

nx.draw(
    graph,
    pos=nx.spectral_layout(graph),
    nodecolor='g',
    edge_color='b'
)

# Для отображения графа нужен numpy и matplotlib/graphviz.
plt.show()
