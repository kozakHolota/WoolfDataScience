from math import fsum
from os import PathLike
from typing import Tuple, List


def total_salary(path: PathLike) -> Tuple[float, float]:
    """
    1. Читаємо файл з параметру
    2. Кожен рядок розділяємо по комі, беремо 2-ге значення зарплати та переводимо у дріб з плаваючою точкою
    3. Сумуємо всі зарплати
    4. Знаходимо середнє арифметичне
    :param path: Шлях до файлу з працівниками
    :return: середню зарплату
    """

    with open(path, 'r') as file:
        salaries = [float(line.split(',')[1]) for line in file]

        return fsum(salaries), fsum(salaries) / len(salaries)

def get_cats_info(path: PathLike) -> List[dict]:
    with open(path, 'r') as file:
        cats: List[dict] = []
        for line in file:
            cats.append({
                'id': line.split(',')[0],
                'name': line.split(',')[1],
                'age': int(line.split(',')[2])
            })
        return cats

if __name__ == '__main__':
    sal_sum, avg_salary = total_salary('workers_salaries.txt')
    print(f"Завдання №1. Загальна та середня зарплата працівників з файлу 'workers_salaries.txt'\n Загальна: {sal_sum:.2f}, Середня: {avg_salary:.2f}")

    cats_info = get_cats_info('cats.txt')
    print("Завдання №2. Виводимо інформацію про котів")
    print(10 * "=")
    mapping = {'id': 'Ідентифікатор', 'name': 'Імʼя', 'age': 'Вік'}
    for cat in cats_info:
        for key in cat:
            print(f"{mapping[key]}: {cat[key]}")
        print(10*"=")