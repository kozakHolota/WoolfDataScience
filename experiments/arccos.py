import plotly.graph_objects as go
import numpy as np


def dot_product(vector1_start, vector1_end, vector2_start, vector2_end):
    # Обчислюємо вектори
    vector1 = np.array(vector1_end) - np.array(vector1_start)
    vector2 = np.array(vector2_end) - np.array(vector2_start)


    # Обчислюємо скалярний добуток
    scalar_product = np.dot(vector1, vector2)


    return scalar_product



# Задаємо координати векторів
vector1_start = [1, 2]
vector1_end = [4, 6]


vector2_start = [3, 1]
vector2_end = [6, 3]


print(dot_product(vector1_start, vector1_end, vector2_start, vector2_end))
