import random
from timeit import timeit

from home_works.algorithms_data_structures.homework_3.util import insertion_sort, merge_sort, draw_sort_algs_graph, \
    write_alg_data, draw_sort_functions_grow_speed


def main():
    data_amount_data = []
    insert_alg_values = []
    merge_alg_values = []
    timeit_alg_values = []
    for i in range(10, 500, 25):
        data_amount_data.append(i)
        array = random.choices(range(10000), k=i)
        insert_alg_value = timeit(lambda: insertion_sort(array))
        merge_alg_value = timeit(lambda: merge_sort(array))
        timeit_alg_value = timeit(lambda: sorted(array))
        insert_alg_values.append(insert_alg_value)
        merge_alg_values.append(merge_alg_value)
        timeit_alg_values.append(timeit_alg_value)
        print(f"Час виконання алгоритму сортування вставками масиву в {i} елементів: {insert_alg_value}")
        print(f"Час виконання алгоритму сортування обʼєднанням в {i} елементів: {merge_alg_value}")
        print(f"Час виконання алгоритму сортування Timeit в {i} елементів: {timeit_alg_value}")
        print("="*20)

    draw_sort_algs_graph(data_amount_data, insert_alg_values, merge_alg_values, timeit_alg_values)
    write_alg_data(data_amount_data, insert_alg_values, merge_alg_values, timeit_alg_values)
    draw_sort_functions_grow_speed(data_amount_data, insert_alg_values, merge_alg_values, timeit_alg_values)

if __name__ == "__main__":
    main()