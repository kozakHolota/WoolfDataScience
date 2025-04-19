import re
from typing import Callable, Generator


def caching_fibonacci() -> Callable[[int], int]:
    cache = {}
    def fibonacci(n: int) -> int:
        def cache_finding(n: int) -> int:
            print(f"Число {n} не закешоване, кешуємо фібоначчі для нього")
            cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
            return cache[n]

        if n <= 0:
            return 0
        elif n == 1:
            return 1
        else:
            return cache[n] if n in cache else cache_finding(n)

    return fibonacci

def generator_numbers(text: str) -> Generator[float, None, None]:
    numbers = re.findall(r"[-+]?\d*\.\d+", text)
    for number in numbers:
        yield float(number)

def sum_profit(text: str, func: Callable) -> float:
    return sum(func(text))



if __name__ == "__main__":
    print("Завдання №1")
    fibonacci = caching_fibonacci()
    print("Фібоначчі для числа 10: ", fibonacci(10))
    print("Фібоначчі для числа 15: ", fibonacci(15))
    print("Завдання №2")
    text = "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів."
    total_income = sum_profit(text, generator_numbers)
    print(f"Загальний дохід: {total_income}")
