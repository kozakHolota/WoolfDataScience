import networkx as nx

from home_works.algorithms_data_structures.homework_5.util import draw_graph, \
    get_task_graph

if __name__ == "__main__":
    transport_graph = get_task_graph()
    draw_graph(transport_graph, "Фейковий граф транспортної сітки міста Львів")
    print("Граф має " + str(transport_graph.number_of_nodes()) + " вершин")
    print("Граф має " + str(transport_graph.number_of_edges()) + " ребер")
    print("Середня довжина шляху у графі: " + str(nx.average_shortest_path_length(transport_graph)))