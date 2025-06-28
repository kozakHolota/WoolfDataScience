import heapq
import random
from collections import deque

import networkx as nx
from matplotlib.pyplot import title

from home_works.algorithms_data_structures.final_project.util import get_heap_graph, draw_tree


def dfs_edges(graph: nx.DiGraph | nx.Graph, source: str, visited=None) -> list:
    dfs_paths = []
    visited = set() if visited is None else visited
    visited.add(source)

    root_successors = graph.successors(source) if isinstance(graph, nx.DiGraph) else graph.neighbors(source)

    for root_successor in root_successors:
        if root_successor not in visited:
            dfs_paths.append((source, root_successor))
            dfs_paths.extend(dfs_edges(graph, root_successor, visited))

    return dfs_paths

def bfs_edges(graph: nx.DiGraph | nx.Graph, source: str) -> list:
    visited = set()
    visited.add(source)
    bfs_paths = []
    queue = deque([source])
    while queue:
        vertex = queue.popleft()
        for neighbor in graph.neighbors(vertex):
            if neighbor not in visited:
                visited.add(neighbor)
                bfs_paths.append((vertex, neighbor))
                queue.append(neighbor)

    return bfs_paths

def color_graph(graph: nx.DiGraph | nx.Graph, paths: list) -> nx.DiGraph | nx.Graph:
    color = 1208288
    nodes_order = []
    for path in paths:
        if not path[0] in nodes_order:
            nodes_order.append(path[0])
        if not path[1] in nodes_order:
            nodes_order.append(path[1])

    for path in nodes_order:
        graph.nodes[path]["color"] = "#" + hex(color).replace("0x", "")
        color += 1500

    return graph

if __name__ == "__main__":
    data = random.sample(range(100), k=10)
    heapq.heapify(data)
    heap_tree_graph = get_heap_graph(data)
    draw_tree(heap_tree_graph)
    bfs_path_graph = color_graph(heap_tree_graph, bfs_edges(heap_tree_graph, data[0]))
    draw_tree(bfs_path_graph, title="BFS Visited Graph")
    dfs_path_graph = color_graph(heap_tree_graph, dfs_edges(heap_tree_graph, data[0]))
    draw_tree(dfs_path_graph, title="DFS Visited Graph")