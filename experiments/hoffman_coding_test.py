import heapq
import collections


class Node:
    def __init__(self, symbol=None, frequency=0, left=None, right=None):
        self.symbol = symbol
        self.frequency = frequency
        self.left = left
        self.right = right


    def __lt__(self, other):
        return self.frequency < other.frequency


def build_huffman_tree(text):
    # Підрахунок частот символів у тексті
    frequencies = collections.Counter(text)


    # Створення вузлів для кожного символу
    priority_queue = [Node(symbol=s, frequency=f) for s, f in frequencies.items()]
    heapq.heapify(priority_queue)


    # Побудова кодового дерева
    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)
        merged_node = Node(frequency=left.frequency + right.frequency, left=left, right=right)
        heapq.heappush(priority_queue, merged_node)


    return priority_queue[0]


def build_huffman_codes(node, current_code="", codes={}):
    # Рекурсивна побудова кодів для кожного символу
    if node.symbol is not None:
        codes[node.symbol] = current_code
    if node.left is not None:
        build_huffman_codes(node.left, current_code + "0", codes)
    if node.right is not None:
        build_huffman_codes(node.right, current_code + "1", codes)


def huffman_encoding(text):
    # Побудова кодового дерева
    root = build_huffman_tree(text)


    # Побудова кодів для кожного символу
    codes = {}
    build_huffman_codes(root, "", codes)


    # Кодування тексту за отриманими кодами
    encoded_text = ''.join(codes[char] for char in text)


    return encoded_text, codes


# Приклад використання
text_example = "aaaaaaaaaaeeeeeeeeeeeeeeeiiiiiiiiiiiiooouuuussssssssssssst"
encoded_text, huffman_codes = huffman_encoding(text_example)


huffman_codes = dict(sorted(huffman_codes.items()))


print("Схема кодування:")
for symbol, code in huffman_codes.items():
    print(f"'{symbol}': {code}")


print("Закодований текст:", encoded_text)
