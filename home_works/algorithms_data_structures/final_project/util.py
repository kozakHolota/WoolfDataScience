import heapq

import networkx as nx
from matplotlib import pyplot as plt

def get_heap_graph(heap_list: list):
    graph = nx.Graph()
    for i in range(len(heap_list)):
        # Додаємо вузол з обов’язковими атрибутами color та label
        graph.add_node(heap_list[i],
                       weight=heap_list[i],
                       color="lightblue",    # стандартний колір
                       label=str(heap_list[i]))  # мітка = значення вузла текстом
        left = 2 * i + 1
        right = 2 * i + 2
        if left < len(heap_list):
            graph.add_edge(heap_list[i], heap_list[left], label="left", weight=1)
        if right < len(heap_list):
            graph.add_edge(heap_list[i], heap_list[right], label="right", weight=1)
    return graph

def dijkstra_shortest_path(graph: nx.Graph, source: int, target: int):
    heap = [(0, source)]
    dist = {v: float("infinity") for v in graph.nodes()}
    prev = {v: None for v in graph.nodes()}
    dist[source] = 0
    while heap:
        current_distance, current_node = heapq.heappop(heap)
        if current_node == target:
            break
        for neighbor in graph[current_node]:
            weight = graph[current_node][neighbor]['weight']
            new_distance = current_distance + weight
            if new_distance < dist[neighbor]:
                dist[neighbor] = new_distance
                prev[neighbor] = current_node
                heapq.heappush(heap, (new_distance, neighbor))
    # Відновлення маршруту
    path = []
    node = target
    if dist[node] < float('infinity'):
        while node is not None:
            path.append(node)
            node = prev[node]
        path.reverse()
    return dist[target], path


def draw_tree(tree, title: str = "Tree Graph"):
    colors = [node[1].get('color', 'lightblue') for node in tree.nodes(data=True)]
    labels = {node[0]: node[1].get('label', str(node[0])) for node in tree.nodes(data=True)}
    # Для дерева краще використовувати graphviz_layout, якщо воно доступне
    try:
        pos = nx.nx_pydot.graphviz_layout(tree, prog='dot')
    except ImportError:
        pos = nx.spring_layout(tree)
    plt.figure(figsize=(8, 5))
    plt.title(title)
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=2500, node_color=colors)
    plt.show()
