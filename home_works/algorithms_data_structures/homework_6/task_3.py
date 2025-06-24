from home_works.algorithms_data_structures.homework_6.util import generate_random_avl_tree, AVLTree, AVLNode

def _sum_node_weights(node):
    if node is None:
        return 0
    return node.key + _sum_node_weights(node.left) + _sum_node_weights(node.right)

def sum_all_weights(tree: AVLTree):
    if tree is None or tree.avl_node is None:
        return 0
    return _sum_node_weights(tree.avl_node)

if __name__ == "__main__":
    avl_tree = generate_random_avl_tree()
    avl_tree.draw()
    print(f"Сума всіх ваг дерева: {sum_all_weights(avl_tree)}")