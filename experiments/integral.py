import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.lines import Line2D


# Задаємо функцію
def func(x):
     return x**3 - 15 * x**2 + 71*x - 20



# Границі інтегрування
a, b = 2, 9  # integral limits
# Діапазон зміни x
x = np.linspace(0, 10)
# Розраховуємо значення y
y = func(x)

y_a = func(a)
y_b = func(b)


fig, ax = plt.subplots()
ax.plot(x, y, 'r', linewidth=2)
ax.set_ylim(bottom=0)

# Додаємо горизонтальні лінії до осі y
ax.add_line(Line2D([0, a], [y_a, y_a], color='blue', linewidth=1))  # Горизонтальна лінія для y_a
ax.add_line(Line2D([0, b], [y_b, y_b], color='yellow', linewidth=1))  # Горизонтальна лінія для y_b


# Оформлюємо область
# Генеруємо значення x та y в області інтегрування
ix = np.linspace(a, b)
iy = func(ix)


# Зафарбовуємо область
verts = [(a, 0), *zip(ix, iy), (b, 0)]
poly = Polygon(verts, facecolor='0.9', edgecolor='0.5')
ax.add_patch(poly)


# Розміщуємо текст інтеграла всередині області
ax.text(0.5 * (a + b), 30, r"$\int_2^9 (x^3 - 15x^2 + 71x - 20)dx$",
           horizontalalignment='center', fontsize=20)


# Підписуємо осі
fig.text(0.9, 0.05, '$x$')
fig.text(0.1, 0.9, '$y$')


# Ховаємо верхню та праву границі
ax.spines[['top', 'right']].set_visible(False)


# Змінюємо підписи на осях
ax.set_xticks([a, b], labels=[f'$x_a = {a}$', f'$x_b = {b}$'])
ax.set_yticks([y_a, y_b], labels=[f'$y_a = {y_a}$', f'$y_b = {y_b}$'])


plt.show()