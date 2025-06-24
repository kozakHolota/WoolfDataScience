import networkx as nx

from home_works.algorithms_data_structures.homework_6.util import generate_random_avl_tree, AVLTree


def find_min_node(avl_tree: AVLTree):
    avl_tree_graph: nx.DiGraph = avl_tree.graph
    left_node = avl_tree.avl_node.left
    if not left_node:
        return avl_tree_graph.nodes[avl_tree.avl_node]["weight"]

    return next(filter(lambda n: n.left is None, [left_node, *avl_tree_graph.successors(left_node)]))

if __name__ == "__main__":
    avl_tree = generate_random_avl_tree()
    avl_tree.draw()
    print(f"Нода з найменшою вагою: {find_min_node(avl_tree)}")