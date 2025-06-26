import copy
import heapq
import random

import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout


def get_connect_wires_heap(wires: list):
    h_wires = copy.deepcopy(wires)
    heapq.heapify(h_wires)
    return h_wires

def get_heap_graph(heap_list: list):
    graph = nx.Graph()
    for i in range(len(heap_list)):
        graph.add_node(heap_list[i])
        left = 2 * i + 1
        right = 2 * i + 2
        if left < len(heap_list):
            graph.add_edge(heap_list[i], heap_list[left], label="left")
        if right < len(heap_list):
            graph.add_edge(heap_list[i], heap_list[right], label="right")

    return graph

def draw_graph(wires_heap_list: list, title: str):
    graph = get_heap_graph(wires_heap_list)
    pos = nx.spring_layout(graph)

    plt.figure(figsize=(10, 8))
    nx.draw(graph, pos, with_labels=True,
            node_color='lightblue',
            node_size=500,
            arrows=True)

    edge_labels = nx.get_edge_attributes(graph, 'label')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)

    plt.title(title)
    plt.axis('off')
    plt.show()

def get_wires_connectors_count(wires_heap_list: list):
    graph = get_heap_graph(wires_heap_list)
    return len({w[0] for w in graph.edges()})


if __name__ == "__main__":
    wires = random.choices(range(1, 100), k=random.randint(1, 10))
    wires_connetion = get_connect_wires_heap(wires)
    print(f"Список кабелів (по довжинах): {wires}")
    print(f"Кількість зґєднувачів, необхідна для зʼєднання всіх кабелів: {get_wires_connectors_count(wires_connetion)}")
    draw_graph(wires_connetion, title="Графік зєднання вибраних мережевих кабелів")
