import networkx as nx
import matplotlib.pyplot as plt


# Створення зваженого графа
weighted_graph = nx.Graph()
weighted_graph.add_weighted_edges_from([(1, 2, 3), (2, 3, 2), (3, 4, 1), (4, 5, 4)])


# Визначення позицій вершин для візуалізації
pos = nx.spring_layout(weighted_graph)


# Витягнення ваг кожного ребра
edge_labels = {(u, v): d["weight"] for u, v, d in weighted_graph.edges(data=True)}


# Візуалізація зваженого графа
nx.draw(weighted_graph, pos, with_labels=True, font_size=10, node_size=700, node_color='skyblue', font_color='black', edge_color='gray')
nx.draw_networkx_edge_labels(weighted_graph, pos, edge_labels=edge_labels, font_color='red', font_size=8)


plt.title("Weighted Graph")
plt.show()
