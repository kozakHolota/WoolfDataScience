import networkx as nx
import matplotlib.pyplot as plt


# Створення пустого графа
G = nx.Graph()


# Додавання вершин
G.add_nodes_from([1, 2, 3, 4, 5])


# Додавання ребер (з'єднань між вершинами)
G.add_edges_from([(1, 2), (1, 3), (2, 4), (2, 5)])


# Візуалізація графа
pos = nx.spring_layout(G)  # Визначення позицій вершин
nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', font_size=10, edge_color='gray')
plt.show()