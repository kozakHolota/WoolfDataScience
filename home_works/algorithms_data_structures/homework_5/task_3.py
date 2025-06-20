import networkx as nx
from networkx.classes import nodes
from sympy.multipledispatch.dispatcher import source

from home_works.algorithms_data_structures.homework_5.util import get_task_graph


def dijkstra_shortest_path(graph: nx.Graph|nx.DiGraph, source: str, target: str):
    distance_to_source = 0
    current_node = source
    processed_nodes = []
    nearest_neibours = nx.descendants(graph, source)
    while current_node != target:
        node_distances = {node: graph.get_edge_data(current_node, node)["weight"] + distance_to_source for node in nearest_neibours if graph.get_edge_data(current_node, node) is not None}
        current_node = min(node_distances, key=node_distances.get)
        distance_to_source = node_distances[current_node]
        processed_nodes.append(current_node)
        nearest_neibours = nx.descendants(graph, current_node)

    return distance_to_source, [source, *processed_nodes]

if __name__ == "__main__":
    lviv_transport_graph = get_task_graph()
    source = "Аеропорт"
    target = "Шевченківський гай"
    distance, path = dijkstra_shortest_path(lviv_transport_graph, source, target)
    control_path = nx.dijkstra_path(lviv_transport_graph, source, target)
    controle_distance = nx.dijkstra_path_length(lviv_transport_graph, source, target)
    print(f"Найкоротший шлях, знайдений нашою реалізацією алгоритму Дейкстри: {path}. Відстань: {distance}")
    print(f"Контрольний виклик реалізації алгоритму Дейкстри в бібліотеці networkx: {control_path}. Відстань: {controle_distance}")


