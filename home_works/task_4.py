import re
from datetime import datetime
import random

from typing import List


def get_days_from_today(date: str) -> int:
    return (datetime.today() - datetime.strptime(date, "%Y-%m-%d")).days

def get_numbers_ticket(min: int, max: int, quantity: int) -> list:
    real_quantity = max - min
    if quantity >= real_quantity:
        raise ValueError(f"Загальна кількість номерів {quantity} перевищує реальну кількість унікальних значень: {real_quantity}")
    lottery_numbers = random.choices(range(min, max), k=quantity)
    lottery_numbers.sort()
    return lottery_numbers

def normalize_phone(phone_number: str) -> str:
    return re.sub(
        r'(^[+38]*)(\d+)',
        r'+38\2',
        re.sub(r"[^+0-9]", "", phone_number)
    )

def get_upcoming_birthdays(users: List[dict]) -> List[dict]:
    today_date = datetime.today()
    def user_birthday_check(user):
        user_bdate = datetime.strptime(user["birthday"], "%Y.%m.%d")
        test_ddate = user_bdate.replace(year=today_date.year)
        return (today_date - test_ddate).days < 7

    return list(filter(user_birthday_check, users))


if __name__ == "__main__":
    test_date = "2023-01-01"
    print(f"Завдання №1. Різниця між датою '{test_date}' і сьогодні: ", get_days_from_today(test_date))
    print("Завдання №2. І ось кубики з нашого лототрону: ", get_numbers_ticket(1, 100, 10))

    print("Завдання №3")
    phones = [
    "067\\t123 4567",
    "(095) 234-5678\\n",
    "+380 44 123 4567",
    "380501234567",
    "    +38(050)123-32-34",
    "     0503451234",
    "(050)8889900",
    "38050-111-22-22",
    "38050 111 22 11   ",
    ]

    for phone in phones:
        print("Оригінальний телефон: ", phone, ", коректний телефон: ", normalize_phone(phone))

    users = [
        {"name": "John Doe", "birthday": "1985.01.23"},
        {"name": "Jane Smith", "birthday": "1990.01.27"},
        {"name": "Jane Austin", "birthday": "1720.03.5"},
        {"name": "Jane Doe", "birthday": "1979.03.8"},
    ]

    print(f"Завдання №4. Сучасна дата: {datetime.today().strftime('%Y-%m-%d')}. Працівники, що мають день народження цього тижня: {get_upcoming_birthdays(users)}")
    print("Завдання №2. І ось кубики з нашого неправильного лототрону: ", get_numbers_ticket(1, 10, 9))
