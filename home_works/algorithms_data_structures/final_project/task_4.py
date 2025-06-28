import heapq
import random

from home_works.algorithms_data_structures.final_project.util import get_heap_graph, draw_tree

if __name__ == "__main__":
    data = random.sample(range(100), k=10)
    heapq.heapify(data)
    print(data)
    heap_tree_graph = get_heap_graph(data)
    draw_tree(heap_tree_graph)