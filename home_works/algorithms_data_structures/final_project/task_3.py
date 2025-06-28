import heapq
import random

from home_works.algorithms_data_structures.final_project.util import get_heap_graph, draw_tree, dijkstra_shortest_path

if __name__ == "__main__":
    data = random.sample(range(100), k=15)
    heapq.heapify(data)  # heapify змінює data in-place та повертає None
    heap_tree_graph = get_heap_graph(data)  # передаємо вже створену купу як список
    draw_tree(heap_tree_graph)
    for i in data[1:]:
        distance, path = dijkstra_shortest_path(heap_tree_graph, data[0], i)
        print(f"Найкоротший шлях від початкової ноди {data[0]} до {i} за алгоритмом Дейкстри: {path}. Дистанція: {distance}")