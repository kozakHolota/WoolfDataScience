import plotly.graph_objects as go
import numpy as np


# Створення двох компланарних векторів
vector_a = np.array([2, 3, 1])
vector_b = np.array([1, 4, 2])


# Знаходження нормалі до площини, утвореної векторами
normal_vector = np.cross(vector_a, vector_b)


# Створення масиву точок у площині
point_in_plane = np.array([0, 0, 0])
points_on_plane = np.column_stack((vector_a, vector_b, normal_vector)) + point_in_plane


# Створення об'єкта "Figure" для 3D графіка
fig = go.Figure()


# Додавання векторів до графіка
fig.add_trace(go.Scatter3d(x=[0, vector_a[0]], y=[0, vector_a[1]], z=[0, vector_a[2]],
                           mode='lines+markers', marker=dict(size=5), line=dict(color='red'), name='Вектор A'))
fig.add_trace(go.Scatter3d(x=[0, vector_b[0]], y=[0, vector_b[1]], z=[0, vector_b[2]],
                           mode='lines+markers', marker=dict(size=5), line=dict(color='blue'), name='Вектор B'))
fig.add_trace(go.Scatter3d(x=[0, normal_vector[0]], y=[0, normal_vector[1]], z=[0, normal_vector[2]],
                           mode='lines+markers', marker=dict(size=5), line=dict(color='green'), name='Нормаль'))


# Додавання площини до графіка
xx, yy = np.meshgrid(np.linspace(-2, 4, 5), np.linspace(-2, 4, 5))
zz = (-normal_vector[0] * xx - normal_vector[1] * yy - point_in_plane[2]) / normal_vector[2]
fig.add_trace(go.Surface(x=xx, y=yy, z=zz, opacity=0.3, colorscale='gray', name='Площина'))


# Налаштування вигляду графіка
fig.update_layout(scene=dict(aspectmode='data'))
fig.update_layout(scene=dict(xaxis_title='Вісь X', yaxis_title='Вісь Y', zaxis_title='Вісь Z'))
fig.update_layout(title='Компланарні вектори, що лежать у площині, та нормаль до площини')


# Відображення графіка
fig.show()
