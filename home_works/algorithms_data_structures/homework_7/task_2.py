import heapq
import random
from functools import reduce
from typing import List


def heap_sort(iterable, descending=False):
    # Визначаємо, який знак використовувати залежно від порядку сортування
    sign = -1 if descending else 1

    # Створюємо купу, використовуючи заданий порядок сортування
    h = [sign * el for el in iterable]
    heapq.heapify(h)
    # Витягуємо елементи, відновлюємо їхні оригінальні значення (якщо потрібно) і формуємо відсортований масив
    return [sign * heapq.heappop(h) for _ in range(len(h))]

def merge_and_sort(iterable: List[List]):
    return heap_sort(reduce(lambda a, b: a + b, iterable))


if __name__ == "__main__":
    start_list = [random.choices(random.randint(2, 20), k=random.randint(1, 10)) for _ in range(1, 20)]
    print(f"Сира колекція: {start_list}")
    sorted_list = merge_and_sort(start_list)
    print(f"Відсортована колекція: {sorted_list}")