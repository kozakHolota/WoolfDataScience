import networkx as nx

from home_works.algorithms_data_structures.homework_6.util import generate_random_avl_tree, AVLTree


def find_max_node(avl_tree: AVLTree):
    avl_tree_graph: nx.DiGraph = avl_tree.graph
    right_node = avl_tree.avl_node.right
    if not right_node:
        return avl_tree.avl_node.key

    return next(filter(lambda n: n.right is None, [right_node, *avl_tree_graph.successors(right_node)]))

if __name__ == "__main__":
    avl_tree = generate_random_avl_tree()
    avl_tree.draw()
    print(f"Нода з найбільшою вагою: {find_max_node(avl_tree)}")