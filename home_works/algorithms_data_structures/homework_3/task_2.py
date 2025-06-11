import random
from typing import List

from home_works.algorithms_data_structures.homework_3.util import merge_sort


def merge_sort_k_lists(lists: List[List]) -> List:
    combined_list = [item for sublist in lists for item in sublist]
    return merge_sort(combined_list)


if __name__ == "__main__":
    lists = [sorted(random.choices(range(10000), k=random.randint(1, 10))) for _ in range(1, 6)]
    print("Сирі дані")
    print(lists)
    print("Відсортований список")
    print(merge_sort_k_lists(lists))
