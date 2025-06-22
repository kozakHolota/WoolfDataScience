from collections import deque
from typing import Tuple

import networkx as nx

from home_works.algorithms_data_structures.homework_5.util import get_task_graph

def dfs_edges(graph: nx.DiGraph | nx.Graph, source: str, visited=None) -> list:
    dfs_paths = []
    visited = set() if visited is None else visited
    visited.add(source)

    # Fetch successors for directed or undirected graphs
    root_successors = graph.successors(source) if isinstance(graph, nx.DiGraph) else graph.neighbors(source)

    for root_successor in root_successors:
        if root_successor not in visited:
            dfs_paths.append((source, root_successor))
            dfs_paths.extend(dfs_edges(graph, root_successor, visited))  # Recursive call with updated visited set

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

def get_control_dfs_bfs_paths(graph: nx.DiGraph | nx.Graph, source: str) -> Tuple[list, list]:
    dfs_path = list(nx.dfs_edges(graph, source))
    bfs_path = list(nx.bfs_edges(graph, source))
    return dfs_path, bfs_path

if __name__ == "__main__":
    transport_graph = get_task_graph()
    control_dfs_path, control_bfs_path = get_control_dfs_bfs_paths(transport_graph, "Аеропорт")
    dfs_path = dfs_edges(transport_graph, "Аеропорт")
    bfs_path = bfs_edges(transport_graph, "Аеропорт")
    print("DFS from our implementation: " + str(dfs_path))
    print("Control DFS from networkx library: " + str(control_dfs_path))
    print("BFS from our implementation: " + str(bfs_path))
    print("Control BFS from networkx library: " + str(control_bfs_path))