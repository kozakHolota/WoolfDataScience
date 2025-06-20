from typing import Tuple

import networkx as nx

from home_works.algorithms_data_structures.homework_5.util import get_task_graph

def get_dfs_bfs_paths(graph: nx.DiGraph | nx.Graph, source: str) -> Tuple[list, list]:
    dfs_path = list(nx.dfs_edges(graph, source))
    bfs_path = list(nx.bfs_edges(graph, source))
    return dfs_path, bfs_path

if __name__ == "__main__":
    transport_graph = get_task_graph()
    dfs_path, bfs_path = get_dfs_bfs_paths(transport_graph, "Аеропорт")
    print("DFS: "+ str(dfs_path))
    print("BFS: "+ str(bfs_path))