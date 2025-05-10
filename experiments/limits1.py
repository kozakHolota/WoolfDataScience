import math

from sympy import *
import matplotlib.pyplot as plt
import numpy as np

X = symbols('x')
x = np.arange(-50, 50, 0.01)

def draw_plot(func):
    # Data for plotting
    x_axis = np.arange(-50, 50, 0.01)
    y_axis = func

    fig, ax = plt.subplots()
    ax.plot(x_axis, y_axis)

    ax.set(xlabel='x', ylabel='y',
           title='xy Graph')
    ax.grid()

    plt.show()

def solve_limit_analytically(func):
    return limit(func, X, oo)

functions = {
    "(4*x**3 - 2*x**2 + x - 2) / (2*x**3 + 6*x**2 - 3*x)": (
        (4*x**3 - 2*x**2 + x - 2) / (2*x**3 + 6*x**2 - 3*x),
        (4*X**3 - 2*X**2 + X - 2) / (2*X**3 + 6*X**2 - 3*X)
    ),
    "(x - x**2) / sin(x)": (
        (x - x**2) / np.sin(x),
        (X - X**2) / sin(X)
    )
}

for func in functions:
    draw_plot(functions[func][0])
    print(f"Numerical limit of {func} is {limit(functions[func][1], X, oo)}")