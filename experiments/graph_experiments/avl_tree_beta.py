import networkx as nx
from matplotlib import pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout

class AVLTree(nx.DiGraph):
    """
    AVL-дерево на основі NetworkX DiGraph із малюванням, балансуванням, захищеною мапою батьків і явною перевіркою унікальності вузлів.
    """

    RIGHT_LABEL = "right"
    LEFT_LABEL = "left"

    def __init__(self):
        super().__init__()
        self.root = None
        self._parent = {}

    def get_height(self, node):
        if node is None or node not in self.nodes:
            return -1
        return self.nodes[node].get("height", 0)

    def update_height(self, node):
        if node in self.nodes:
            left_height = self.get_height(self.get_left(node))
            right_height = self.get_height(self.get_right(node))
            self.nodes[node]["height"] = 1 + max(left_height, right_height)

    def get_balance_factor(self, node):
        return self.get_height(self.get_left(node)) - self.get_height(self.get_right(node))

    def get_left(self, node):
        if node not in self:
            return None
        for succ, data in self[node].items():
            if data.get("label") == self.LEFT_LABEL:
                return succ
        return None

    def get_right(self, node):
        if node not in self:
            return None
        for succ, data in self[node].items():
            if data.get("label") == self.RIGHT_LABEL:
                return succ
        return None

    def set_child(self, parent, child, label):
        if parent not in self:
            return
        old_child = self.get_left(parent) if label == self.LEFT_LABEL else self.get_right(parent)
        if old_child is not None:
            self.remove_edge(parent, old_child)
            if self._parent.get(old_child) == parent:
                del self._parent[old_child]
        if child is not None:
            self.add_edge(parent, child, label=label)
            self._parent[child] = parent

    def get_parent(self, node):
        return self._parent.get(node, None)

    def rotate_left(self, z):
        y = self.get_right(z)
        if y is None:
            return z
        T2 = self.get_left(y)
        parent_z = self.get_parent(z)
        if parent_z is None:
            self.root = y
        else:
            if self.get_left(parent_z) == z:
                self.set_child(parent_z, y, self.LEFT_LABEL)
            else:
                self.set_child(parent_z, y, self.RIGHT_LABEL)
        self.set_child(y, z, self.LEFT_LABEL)
        self.set_child(z, T2, self.RIGHT_LABEL)
        self.update_height(z)
        self.update_height(y)
        return y

    def rotate_right(self, z):
        y = self.get_left(z)
        if y is None:
            return z
        T3 = self.get_right(y)
        parent_z = self.get_parent(z)
        if parent_z is None:
            self.root = y
        else:
            if self.get_left(parent_z) == z:
                self.set_child(parent_z, y, self.LEFT_LABEL)
            else:
                self.set_child(parent_z, y, self.RIGHT_LABEL)
        self.set_child(y, z, self.RIGHT_LABEL)
        self.set_child(z, T3, self.LEFT_LABEL)
        self.update_height(z)
        self.update_height(y)
        return y

    def rebalance(self, node):
        self.update_height(node)
        balance = self.get_balance_factor(node)
        if balance > 1:
            if self.get_balance_factor(self.get_left(node)) < 0:
                self.rotate_left(self.get_left(node))
            return self.rotate_right(node)
        if balance < -1:
            if self.get_balance_factor(self.get_right(node)) > 0:
                self.rotate_right(self.get_right(node))
            return self.rotate_left(node)
        return node

    def _insert(self, current, node, weight):
        """Рекурсивна вставка з балансуванням."""
        if current is None:
            if node in self.nodes:
                raise ValueError(f"Вузол {node} вже існує в дереві!")
            super().add_node(node, weight=weight, height=0)
            return node
        if weight < self.nodes[current]["weight"]:
            left_child = self.get_left(current)
            new_left = self._insert(left_child, node, weight)
            if left_child != new_left:
                self.set_child(current, new_left, self.LEFT_LABEL)
        else:
            right_child = self.get_right(current)
            new_right = self._insert(right_child, node, weight)
            if right_child != new_right:
                self.set_child(current, new_right, self.RIGHT_LABEL)
        new_root = self.rebalance(current)
        return new_root

    def insert(self, node, weight=0):
        """Публічний метод для вставки з балансуванням і оновленням кореня."""
        if self.root is None:
            if node in self.nodes:
                raise ValueError(f"Вузол {node} вже існує в дереві!")
            super().add_node(node, weight=weight, height=0)
            self.root = node
            return
        new_root = self._insert(self.root, node, weight)
        while self.get_parent(new_root) is not None:
            new_root = self.get_parent(new_root)
        self.root = new_root

    @property
    def parent_map(self):
        return self._parent.copy()

    def draw(self, with_weights=True):
        """Малює дерево із вагами."""
        if self.root is None:
            print("Дерево порожнє")
            return
        pos = graphviz_layout(self, prog='dot')
        labels = {n: f"{n}\n{self.nodes[n]['weight']}" if with_weights else str(n) for n in self.nodes}
        nx.draw(self, pos, with_labels=True, labels=labels, arrows=False, node_size=2000, node_color="lightblue", font_size=10)
        plt.show()


if __name__ == "__main__":
    print("Створення AVL-дерева та малювання структури після кількох вставок:")
    tree = AVLTree()
    weights = [1, 45, 6, 122, 11, 18, 0, 9, 55, 13, 14, 112]
    for idx, weight in enumerate(weights):
        name = f"N{weight}"
        tree.insert(name, weight)
        print(f"Вставлено вузол {name} з вагою {weight}, root: {tree.root}")
    tree.draw()

    print("Висоти вузлів:")
    for node in tree.nodes:
        print(node, "height:", tree.nodes[node]["height"])