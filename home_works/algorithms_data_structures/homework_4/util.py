import csv
from dataclasses import dataclass
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps

def build_shift_table(pattern):
  """Створити таблицю зсувів для алгоритму Боєра-Мура."""
  table = {}
  length = len(pattern)
  # Для кожного символу в підрядку встановлюємо зсув рівний довжині підрядка
  for index, char in enumerate(pattern[:-1]):
    table[char] = length - index - 1
  # Якщо символу немає в таблиці, зсув буде дорівнювати довжині підрядка
  table.setdefault(pattern[-1], length)
  return table

def polynomial_hash(s, base=256, modulus=101):
    """
    Повертає поліноміальний хеш рядка s.
    """
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value

def kmp_search(main_string, pattern):
    M = len(pattern)
    N = len(main_string)

    lps = compute_lps(pattern)

    i = j = 0

    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1

        if j == M:
            return i - j

    return -1  # якщо підрядок не знайдено

def boyer_moore_search(text, pattern):
  # Створюємо таблицю зсувів для патерну (підрядка)
  shift_table = build_shift_table(pattern)
  i = 0 # Ініціалізуємо початковий індекс для основного тексту

  # Проходимо по основному тексту, порівнюючи з підрядком
  while i <= len(text) - len(pattern):
    j = len(pattern) - 1 # Починаємо з кінця підрядка

    # Порівнюємо символи від кінця підрядка до його початку
    while j >= 0 and text[i + j] == pattern[j]:
      j -= 1 # Зсуваємось до початку підрядка

    # Якщо весь підрядок збігається, повертаємо його позицію в тексті
    if j < 0:
      return i # Підрядок знайдено

    # Зсуваємо індекс i на основі таблиці зсувів
    # Це дозволяє "перестрибувати" над неспівпадаючими частинами тексту
    i += shift_table.get(text[i + len(pattern) - 1], len(pattern))

  # Якщо підрядок не знайдено, повертаємо -1
  return -1

def rabin_karp_search(main_string, substring):
    # Довжини основного рядка та підрядка пошуку
    substring_length = len(substring)
    main_string_length = len(main_string)

    # Базове число для хешування та модуль
    base = 256
    modulus = 101

    # Хеш-значення для підрядка пошуку та поточного відрізка в основному рядку
    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(main_string[:substring_length], base, modulus)

    # Попереднє значення для перерахунку хешу
    h_multiplier = pow(base, substring_length - 1) % modulus

    # Проходимо крізь основний рядок
    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if main_string[i:i + substring_length] == substring:
                return i

        if i < main_string_length - substring_length:
            current_slice_hash = (current_slice_hash - ord(main_string[i]) * h_multiplier) % modulus
            current_slice_hash = (current_slice_hash * base + ord(main_string[i + substring_length])) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus

    return -1

@dataclass
class ResultSet:
    kmp_begin_result_sample_1: float
    kmp_begin_result_sample_2: float
    boyer_moore_begin_result_sample_1: float
    boyer_moore_begin_result_sample_2: float
    rabin_karp_begin_result_sample_1: float
    rabin_karp_begin_result_sample_2: float
    kmp_middle_result_sample_1: float
    kmp_middle_result_sample_2: float
    boyer_moore_middle_result_sample_1: float
    boyer_moore_middle_result_sample_2: float
    rabin_karp_middle_result_sample_1: float
    rabin_karp_middle_result_sample_2: float
    kmp_end_result_sample_1: float
    kmp_end_result_sample_2: float
    boyer_moore_end_result_sample_1: float
    boyer_moore_end_result_sample_2: float
    rabin_karp_end_result_sample_1: float
    rabin_karp_end_result_sample_2: float

    def to_csv_file(self):
        csv_data = [
            ["Алгоритм", "Пошук на початку тексту", "Пошук в середині тексту", "Пошук в кінці тексту"],
            [
                "Кнута-Морріса-Пратта",
                (self.kmp_begin_result_sample_1 + self.kmp_begin_result_sample_2) / 2,
                (self.kmp_middle_result_sample_1 + self.kmp_middle_result_sample_2) / 2,
                (self.kmp_end_result_sample_1 + self.kmp_end_result_sample_2) / 2,
            ],
            [
                "Боєра-Мура",
                (self.boyer_moore_begin_result_sample_1 + self.boyer_moore_begin_result_sample_2) / 2,
                (self.boyer_moore_middle_result_sample_1 + self.boyer_moore_middle_result_sample_2) / 2,
                (self.boyer_moore_end_result_sample_1 + self.boyer_moore_end_result_sample_2) / 2,
            ],
            [
                "Рабіна-Карпа",
                (self.rabin_karp_begin_result_sample_1 + self.rabin_karp_begin_result_sample_2) / 2,
                (self.rabin_karp_middle_result_sample_1 + self.rabin_karp_middle_result_sample_2) / 2,
                (self.rabin_karp_end_result_sample_1 + self.rabin_karp_end_result_sample_2) / 2
            ]
        ]
        
        with open("search_results.csv", "w") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerows(csv_data)
    
    def draw_search_results_graph(self):
        sns.set_theme(style="whitegrid")

        algorithms = ['Кнута-Морріса-Пратта', 'Боєра-Мура', 'Рабіна-Карпа']
        positions = ['Початок', 'Середина', 'Кінець']

        data = {
            'Кнута-Морріса-Пратта': [
                (self.kmp_begin_result_sample_1 + self.kmp_begin_result_sample_2) / 2,
                (self.kmp_middle_result_sample_1 + self.kmp_middle_result_sample_2) / 2,
                (self.kmp_end_result_sample_1 + self.kmp_end_result_sample_2) / 2
            ],
            'Боєра-Мура': [
                (self.boyer_moore_begin_result_sample_1 + self.boyer_moore_begin_result_sample_2) / 2,
                (self.boyer_moore_middle_result_sample_1 + self.boyer_moore_middle_result_sample_2) / 2,
                (self.boyer_moore_end_result_sample_1 + self.boyer_moore_end_result_sample_2) / 2
            ],
            'Рабіна-Карпа': [
                (self.rabin_karp_begin_result_sample_1 + self.rabin_karp_begin_result_sample_2) / 2,
                (self.rabin_karp_middle_result_sample_1 + self.rabin_karp_middle_result_sample_2) / 2,
                (self.rabin_karp_end_result_sample_1 + self.rabin_karp_end_result_sample_2) / 2
            ]
        }

        plt.figure(figsize=(10, 6))

        x = np.arange(len(positions))
        width = 0.25

        for i, (algorithm, values) in enumerate(data.items()):
            plt.bar(x + i * width, values, width, label=algorithm)

        plt.xlabel('Позиція в тексті')
        plt.ylabel('Середній час виконання')
        plt.title('Порівняння часу виконання алгоритмів пошуку')
        plt.xticks(x + width, positions)
        plt.legend()

        plt.show()
    
    def draw_search_results_grow_speed(self):
        sns.set_theme(style="whitegrid")

        positions = np.array([1, 2, 3])  # Begin, Middle, End positions

        kmp_times = np.array([
            (self.kmp_begin_result_sample_1 + self.kmp_begin_result_sample_2) / 2,
            (self.kmp_middle_result_sample_1 + self.kmp_middle_result_sample_2) / 2,
            (self.kmp_end_result_sample_1 + self.kmp_end_result_sample_2) / 2
        ])

        boyer_moore_times = np.array([
            (self.boyer_moore_begin_result_sample_1 + self.boyer_moore_begin_result_sample_2) / 2,
            (self.boyer_moore_middle_result_sample_1 + self.boyer_moore_middle_result_sample_2) / 2,
            (self.boyer_moore_end_result_sample_1 + self.boyer_moore_end_result_sample_2) / 2
        ])

        rabin_karp_times = np.array([
            (self.rabin_karp_begin_result_sample_1 + self.rabin_karp_begin_result_sample_2) / 2,
            (self.rabin_karp_middle_result_sample_1 + self.rabin_karp_middle_result_sample_2) / 2,
            (self.rabin_karp_end_result_sample_1 + self.rabin_karp_end_result_sample_2) / 2
        ])

        kmp_speed = np.gradient(kmp_times, positions)
        boyer_moore_speed = np.gradient(boyer_moore_times, positions)
        rabin_karp_speed = np.gradient(rabin_karp_times, positions)

        plt.figure(figsize=(10, 6))
        plt.plot(positions, kmp_speed, label='Кнута-Морріса-Пратта', marker='o')
        plt.plot(positions, boyer_moore_speed, label='Боєра-Мура', marker='s')
        plt.plot(positions, rabin_karp_speed, label='Рабіна-Карпа', marker='^')

        plt.xlabel('Позиція в тексті')
        plt.ylabel('Швидкість зростання часу')
        plt.title('Порівняння швидкості зростання часу алгоритмів')
        plt.xticks(positions, ['Початок', 'Середина', 'Кінець'])
        plt.legend()
        plt.grid(True)
        plt.show()
        
    def print_results(self):
        print("\nРезультати пошуку:")
        print("\nПошук на початку тексту:")
        print(
            f"Алгоритм Кнута-Морріса-Пратта: {(self.kmp_begin_result_sample_1 + self.kmp_begin_result_sample_2) / 2:.6f} сек")
        print(
            f"Алгоритм Боєра-Мура: {(self.boyer_moore_begin_result_sample_1 + self.boyer_moore_begin_result_sample_2) / 2:.6f} сек")
        print(
            f"Алгоритм Рабіна-Карпа: {(self.rabin_karp_begin_result_sample_1 + self.rabin_karp_begin_result_sample_2) / 2:.6f} сек")

        print("\nПошук в середині тексту:")
        print(
            f"Алгоритм Кнута-Морріса-Пратта: {(self.kmp_middle_result_sample_1 + self.kmp_middle_result_sample_2) / 2:.6f} сек")
        print(
            f"Алгоритм Боєра-Мура: {(self.boyer_moore_middle_result_sample_1 + self.boyer_moore_middle_result_sample_2) / 2:.6f} сек")
        print(
            f"Алгоритм Рабіна-Карпа: {(self.rabin_karp_middle_result_sample_1 + self.rabin_karp_middle_result_sample_2) / 2:.6f} сек")

        print("\nПошук в кінці тексту:")
        print(
            f"Алгоритм Кнута-Морріса-Пратта: {(self.kmp_end_result_sample_1 + self.kmp_end_result_sample_2) / 2:.6f} сек")
        print(
            f"Алгоритм Боєра-Мура: {(self.boyer_moore_end_result_sample_1 + self.boyer_moore_end_result_sample_2) / 2:.6f} сек")
        print(
            f"Алгоритм Рабіна-Карпа: {(self.rabin_karp_end_result_sample_1 + self.rabin_karp_end_result_sample_2) / 2:.6f} сек")
