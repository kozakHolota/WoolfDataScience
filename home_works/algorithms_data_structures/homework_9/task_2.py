import random
from typing import Callable

def is_in_func(x: float, y: float, function: Callable) -> bool:
    return y <= function(x)

def integral_monte_carlo(num_samples: int, min_v: float, max_v: float, function: Callable) -> float:
    inside_plot = 0
    matches = []
    for _ in range(num_samples):
        x = random.uniform(min_v, max_v)
        y = random.uniform(min_v, max_v)
        if is_in_func(x, y, function):
            inside_plot += 1
            matches.append(x)
    approx_integral = (max_v - min_v) * sum(func(x_i) for x_i in matches) / num_samples
    return approx_integral

if __name__ == "__main__":
    import scipy.integrate as spi
    func = lambda x: x**2
    a, b = 0, 10
    monte_carlo_intergals = []
    for i in [1000, 50000, 100000]:
        monte_carlo_intergals.append((i, integral_monte_carlo(i, a, b, func)))
    scipy_integral = spi.quad(func, a, b)

    for i in monte_carlo_intergals:
        print(f"Інтеграл, обчислений після {i[0]} експериментів: {i[1]}")
    print(f"Інтеграл, обчислений за допомогою модуля scipy: {scipy_integral[0]}")
