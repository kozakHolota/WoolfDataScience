import matplotlib.pyplot as plt
import numpy as np


# Створення двох колінеарних векторів
vector_a = np.array([2, 3])
vector_b = 2 * vector_a


# Побудова системи координат і векторів
plt.figure(figsize=(6, 6))
plt.quiver(0, 0, vector_a[0], vector_a[1], angles='xy', scale_units='xy', scale=1, color='r', label='Вектор A')
plt.quiver(0, 1, vector_b[0], vector_b[1], angles='xy', scale_units='xy', scale=1, color='b', label='Вектор B')


# Позначення початку координат
plt.scatter(0, 0, color='black', marker='o')


# Додавання підписів
plt.text(vector_a[0], vector_a[1], ' A', fontsize=12, color='r', va='bottom', ha='left')
plt.text(vector_b[0], vector_b[1], ' B', fontsize=12, color='b', va='bottom', ha='left')


# Налаштування вигляду графіка
plt.xlim(-1, 7)
plt.ylim(-1, 9)
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.grid(color='gray', linestyle='--', linewidth=0.5)
plt.gca().set_aspect('equal', adjustable='box')
plt.title('Колінеарні вектори на площині')
plt.xlabel('Вісь X')
plt.ylabel('Вісь Y')
plt.legend()
plt.show()
