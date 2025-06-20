from pathlib import Path

import pandas as pd
import networkx as nx
from matplotlib import pyplot as plt


def get_transport_connections_graph(nodes_csv: Path, edges_csv: Path):
    # Read and process nodes
    nodes_dict = {row[1]: row[0] for row in pd.read_csv(nodes_csv).itertuples(index=False)}
    nodes = tuple(nodes_dict.values())  # The node IDs will be the keys

    # Read and process edges
    routes_dict = pd.read_csv(edges_csv).to_dict(orient="records")
    routes = []

    for route in routes_dict:
        r_keys = tuple(route.keys())
        for node in r_keys[1:]:
            if pd.notna(route[node] ):
                routes.append((nodes_dict[route[r_keys[0]]], nodes_dict[node], {'weight': int(route[node])}))

    # Create directed graph
    transport_graph = nx.DiGraph()
    transport_graph.add_nodes_from(nodes)  # Use the names as nodes
    transport_graph.add_edges_from(routes)
    return transport_graph

def get_task_graph():
    return get_transport_connections_graph(
        Path(__file__).parent / "lviv_transport_nodes.csv",
        Path(__file__).parent / "node_paths.csv"
    )

def draw_graph(graph: nx.DiGraph | nx.Graph, title: str):
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, font_size=10, node_size=700, node_color='skyblue', font_color='black', edge_color='gray')
    # Draw edge labels (weights)
    edge_labels = nx.get_edge_attributes(graph, 'weight')  # Get weights of edges
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color='red')
    plt.title(title)
    plt.show()