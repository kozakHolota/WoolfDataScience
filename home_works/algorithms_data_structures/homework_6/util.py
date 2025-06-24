import random

import networkx as nx
import matplotlib.pyplot as plt


class AVLNode:
    def __init__(self, key):
        self.key = key
        self.height = 1
        self.left = None
        self.right = None

    def __str__(self, level=0):
        ret = "\t" * level + str(self.key) + "\n"
        if self.left:
            ret += self.left.__str__(level + 1, "L--- ")
        if self.right:
            ret += self.right.__str__(level + 1, "R--- ")
        return ret
    def _get_graph(self):
        graph = nx.DiGraph()
        graph.add_node(self, weight=self.key)
        if self.left:
            graph.add_edge(self, self.left, label="left")
            graph = nx.compose(graph, self.left._get_graph())
        if self.right:
            graph.add_edge(self, self.right, label="right")
            graph = nx.compose(graph, self.right._get_graph())
        return graph

class AVLTree:
    def __init__(self):
        self.avl_node = None  # root

    def __str__(self):
        return str(self.avl_node) if self.avl_node else "<empty tree>"

    @property
    def graph(self):
        return self.avl_node._get_graph()

    def get_height(self, node):
        if not node:
            return 0
        return node.height

    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def left_rotate(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def right_rotate(self, y):
        x = y.left
        T3 = x.right

        x.right = y
        y.left = T3

        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))

        return x

    def min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    # Приватний рекурсивний метод
    def _insert(self, node, key):
        if node is None:
            return AVLNode(key)  # виправлено: повертаємо новий вузол

        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        else:
            # Дублікати не вставляємо
            return node

        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        balance = self.get_balance(node)

        # Ліва-ліва ситуація
        if balance > 1 and key < node.left.key:
            return self.right_rotate(node)

        # Права-права ситуація
        if balance < -1 and key > node.right.key:
            return self.left_rotate(node)

        # Ліва-права ситуація
        if balance > 1 and key > node.left.key:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        # Права-ліва ситуація
        if balance < -1 and key < node.right.key:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def insert(self, key):
        self.avl_node = self._insert(self.avl_node, key)

    def insert_from_list(self, keys):
        for key in keys:
            self.insert(key)

    def delete_node(self, key, node=None):
        if node is None:
            node = self.avl_node
        if not node:
            return node

        if key < node.key:
            node.left = self.delete_node(key, node.left)
        elif key > node.key:
            node.right = self.delete_node(key, node.right)
        else:
            if node.left is None:
                temp = node.right
                node = None
                return temp
            elif node.right is None:
                temp = node.left
                node = None
                return temp

            temp = self.min_value_node(node.right)
            node.key = temp.key
            node.right = self.delete_node(temp.key, node.right)

        if node is None:
            return node

        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        balance = self.get_balance(node)

        # Ліва-ліва
        if balance > 1 and self.get_balance(node.left) >= 0:
            return self.right_rotate(node)

        # Ліва-права
        if balance > 1 and self.get_balance(node.left) < 0:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        # Права-права
        if balance < -1 and self.get_balance(node.right) <= 0:
            return self.left_rotate(node)

        # Права-ліва
        if balance < -1 and self.get_balance(node.right) > 0:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node  # виправлено: повертати node

    def draw(self):
        if not self.avl_node:
            print("Empty tree")
            return

        G = self.avl_node._get_graph()
        pos = nx.spring_layout(G)

        plt.figure(figsize=(10, 8))
        nx.draw(G, pos, with_labels=True, labels={node: node.key for node in G.nodes()},
                node_color='lightblue', node_size=500, arrowsize=20)

        edge_labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        plt.title("AVL Tree Visualization")
        plt.axis('off')
        plt.show()


def generate_random_avl_tree(n: int=random.randint(1, 20), max_val: int=random.randint(1, 10)):
    avl_tree = AVLTree()
    avl_tree.insert_from_list(random.choices(range(max_val), k=n))
    return avl_tree

if __name__ == "__main__":
    avl_tree = AVLTree()
    avl_tree.insert_from_list([1, 45, 6, 122, 11, 18, 0, 9, 55, 13, 14, 112])
    print(avl_tree)
    avl_tree.draw()