import networkx as nx
from matplotlib import pyplot as plt


class AVLTree(nx.DiGraph):
    def __init__(self):
        super().__init__()
        self.root = None

    def get_weight(self, node):
        return self.nodes[node]["weight"]

    def add_node(self, node, weight=0):
        pass

    def add_nodes_from(self, nodes, weight=0):
        for node in nodes:
            self.add_node(node, node["weight"])

    def rotate_left(self, u):
        edges = self.edges(u)

    def rotate_right(self, u):
        edges = self.edges(u)

    def cal_height(self, u):
        return max(self.nodes[u]["height"]) + 1

    def add_edge(self, u_of_edge, v_of_edge, **attr):
        raise ValueError("AVLTree does not support edges")

    def add_edges_from(self, ebunch_to_add, **attr):
        raise ValueError("AVLTree does not support edges")


def draw_tree(tree, root=None, x_spacing=1.5, y_spacing=1):
    """
    Draws a tree structure using NetworkX and a custom hierarchical layout.

    :param tree_edges: List of edges in the tree (e.g. [(parent, child), ...]).
    :param root: Root of the tree; if None, it's determined as the node with no incoming edges.
    :param x_spacing: Horizontal spacing between nodes.
    :param y_spacing: Vertical spacing between levels.
    """

    if root is None:
        # Automatically find the root (a node with no incoming edges)
        root = [n for n in tree.nodes if tree.in_degree(n) == 0][0]

    # Generate positions for the nodes using a custom layout
    pos = hierarchical_position(tree, root, x_spacing, y_spacing)

    # Draw the tree
    plt.figure(figsize=(10, 8))
    nx.draw(
        tree,
        pos,
        with_labels=True,
        node_size=3000,
        node_color="lightblue",
        font_size=10,
        font_weight="bold"
    )

    # Add edge labels if needed (e.g., "left" and "right")
    edge_labels = nx.get_edge_attributes(tree, "label")  # Fetch edge labels, if any
    nx.draw_networkx_edge_labels(tree, pos, edge_labels=edge_labels)

    # Display
    plt.title("AVL Tree Visualization")
    plt.show()


def hierarchical_position(graph, root, x_spacing=1, y_spacing=1):
    """
    Produces a hierarchical layout for a directed tree structure using depth-based positioning.

    :param graph: The NetworkX graph (directed).
    :param root: Root of the tree.
    :param x_spacing: Horizontal distance between sibling nodes.
    :param y_spacing: Vertical distance between levels.
    :return: A position dictionary for all nodes.
    """
    pos = {}  # Dictionary to store node positions
    depths = calculate_depths(graph, root)  # Helper to calculate node depths

    def assign_positions(node, current_x, depth):
        """
        Recursively assign positions to all nodes.
        """
        pos[node] = (current_x, -depth * y_spacing)  # Position the node
        children = list(graph.successors(node))

        if children:
            mid = len(children) // 2  # Determine how to offset child positions
            for i, child in enumerate(children):
                assign_positions(
                    child, current_x + (i - mid) * x_spacing, depth + 1
                )

    assign_positions(root, 0, 0)
    return pos


def calculate_depths(graph, root):
    """
    Helper function to compute the depths of all nodes in a tree.

    :param graph: The NetworkX graph (directed).
    :param root: Root of the tree.
    :return: Dictionary mapping each node to its depth.
    """
    depths = {}

    def dfs(node, depth):
        depths[node] = depth
        for child in graph.successors(node):
            dfs(child, depth + 1)

    dfs(root, 0)
    return depths
