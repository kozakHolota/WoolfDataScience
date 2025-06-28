import random
from io import StringIO

class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    @property
    def last_node(self):
        last_node = None
        cur = self.head
        while cur and cur.next:
            last_node = cur
            cur = cur.next
        return last_node

    def insert_at_beginning(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_at_end(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = new_node

    def insert_after(self, prev_node: Node, data):
        if prev_node is None:
            print("Попереднього вузла не існує.")
            return
        new_node = Node(data)
        new_node.next = prev_node.next
        prev_node.next = new_node

    def delete_node(self, key: int):
        cur = self.head
        if cur and cur.data == key:
            self.head = cur.next
            cur = None
            return
        prev = None
        while cur and cur.data != key:
            prev = cur
            cur = cur.next
        if cur is None:
            return
        prev.next = cur.next
        cur = None

    def search_element(self, data: int):
        cur = self.head
        while cur:
            if cur.data == data:
                return cur
            cur = cur.next
        return None

    def reverse(self):
        prev = None
        current = self.head
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev

    def sort(self):
        if self.head is None or self.head.next is None:
            return

        sorted_head = None

        current = self.head
        while current:
            next_node = current.next

            if (sorted_head is None) or (current.data < sorted_head.data):
                current.next = sorted_head
                sorted_head = current
            else:
                sorted_curr = sorted_head
                while sorted_curr.next and sorted_curr.next.data < current.data:
                    sorted_curr = sorted_curr.next
                current.next = sorted_curr.next
                sorted_curr.next = current

            current = next_node

        self.head = sorted_head

    def merge_and_sort(self, other_list):
        for node in other_list:
            self.insert_at_end(node.data)

        self.sort()

    def __iter__(self):
        cur = self.head
        while cur:
            yield cur
            cur = cur.next

    def __len__(self):
        ln = 0
        cur = self.head
        while cur:
            ln += 1
            cur = cur.next
        return ln

    def __str__(self):
        str_ = StringIO()
        current = self.head
        str_.write("{")
        first = True
        while current:
            if not first:
                str_.write(", ")
            str_.write(str(current.data))
            first = False
            current = current.next
        str_.write("}")
        return str_.getvalue()

if __name__ == "__main__":
    linked_list = LinkedList()
    for i in random.choices(range(10), k=10):
        linked_list.insert_at_end(i)

    print("Початковий звʼязний список: " + str(linked_list))
    linked_list.reverse()
    print("Перевернутий звʼязний список: " + str(linked_list))
    linked_list.sort()
    print("Відсортований список: " + str(linked_list))
    addition_list = LinkedList()
    for i in random.choices(range(10), k=10):
        addition_list.insert_at_end(i)
    print("Додатковий звʼязний список: " + str(addition_list))
    linked_list.merge_and_sort(addition_list)
    print("Після того, як ми до соновного списку додали додатковий та відсортували: " + str(linked_list))