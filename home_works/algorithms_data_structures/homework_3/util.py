import csv

import numpy as np
from matplotlib import pyplot as plt


def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]

    return merge(merge_sort(left_half), merge_sort(right_half))

def merge(left, right):
    merged = []
    left_index = 0
    right_index = 0

    # Спочатку об'єднайте менші елементи
    while left_index < len(left) and right_index < len(right):
        if left[left_index] <= right[right_index]:
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index += 1

    # Якщо в лівій або правій половині залишилися елементи,
		# додайте їх до результату
    while left_index < len(left):
        merged.append(left[left_index])
        left_index += 1

    while right_index < len(right):
        merged.append(right[right_index])
        right_index += 1

    return merged


def insertion_sort(lst):
    for i in range(1, len(lst)):
        key = lst[i]
        j = i-1
        while j >=0 and key < lst[j] :
                lst[j+1] = lst[j]
                j -= 1
        lst[j+1] = key
    return lst

def draw_sort_algs_graph(data_amount_data: list, insert_alg_values: list, merge_alg_values: list, timeit_alg_values: list):
    fig, ax = plt.subplots()

    ax.plot(data_amount_data, insert_alg_values, color='red', label='Алгоритм Вставки')
    ax.plot(data_amount_data, merge_alg_values, color='green', label='Алгоритм Обʼєднання')
    ax.plot(data_amount_data, timeit_alg_values, color='blue', label='Алгоритм Timeit')

    ax.set(xlabel='Кількість даних', ylabel='Час виконання', title='Порівняння часу виконання')
    ax.grid()
    ax.legend()

    plt.show()

def write_alg_data(data_amount_data: list, insert_alg_values: list, merge_alg_values: list, timeit_alg_values: list):
    data_len = len(data_amount_data)

    csv_data = [["Кількість Даних", "Алгоритм Вставки", "Алгоритм Обʼєднання", "Алгоритм Timeit"]]
    for i in range(data_len):
        csv_data.append([data_amount_data[i], insert_alg_values[i], merge_alg_values[i], timeit_alg_values[i]])

    with open("algorithm_comparison.csv", "w") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(csv_data)

def draw_sort_functions_grow_speed(data_amount_data: list, insert_alg_values: list, merge_alg_values: list, timeit_alg_values: list):
    data_amount_data = np.array(data_amount_data)
    insert_alg_values = np.array(insert_alg_values)
    merge_alg_values = np.array(merge_alg_values)
    timeit_alg_values = np.array(timeit_alg_values)

    insert_alg_speed = np.gradient(insert_alg_values, data_amount_data)
    merge_alg_speed = np.gradient(merge_alg_values, data_amount_data)
    timeit_alg_speed = np.gradient(timeit_alg_values, data_amount_data)

    fig, ax = plt.subplots()
    ax.plot(data_amount_data, insert_alg_speed, color='red', label='Алгоритм Вставки')
    ax.plot(data_amount_data, merge_alg_speed, color='green', label='Алгоритм Обʼєднання')
    ax.plot(data_amount_data, timeit_alg_speed, color='blue', label='Алгоритм Timeit')

    ax.set(title='Швидкість зростання функцій алгоритмів')
    ax.grid()
    ax.legend()

    plt.show()

