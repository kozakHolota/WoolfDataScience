import networkx as nx
from matplotlib import pyplot as plt

if __name__ == "__main__":
    G = nx.Graph()
    G.add_nodes_from([1, 2, 3, 4, 5])
    G.add_edges_from([(1, 2), (1, 3), (2, 4), (2, 1), (3, 4), (4, 5)])
    nx.draw(G, with_labels=True)
    plt.show()