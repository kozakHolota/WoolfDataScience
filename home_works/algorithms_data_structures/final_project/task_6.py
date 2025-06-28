from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class FoodItem:
    name: str
    cost: int
    calories: int
    count: int=0

    def __str__(self):
        return f"Найменування: {self.name}, Ціна: {self.cost}, Калорійність: {self.calories}, Кількість: {self.count}"

def get_food_list(food_dict: Dict[str, Dict[str, Any]]) -> List[FoodItem]:
    food_list = []
    for item in food_dict:
        food_list.append(FoodItem(item, **food_dict[item]))
    return sorted(food_list, key=lambda x: x.calories, reverse=True)

def get_food_list_by_budget_greedy(food_dict: Dict[str, Dict[str, Any]], budget: int) -> List[FoodItem]:
    food_list = get_food_list(food_dict)
    for food_item in food_list:
        while food_item.cost <= budget:
            food_item.count += 1
            budget -= food_item.cost

    return list(filter(lambda x: x.count > 0, food_list))

def get_food_list_by_budget_dynamic(food_dict: Dict[str, Dict[str, Any]], budget: int, memo: List[FoodItem] = None) -> List[FoodItem]:
    memo = [] if memo is None else memo
    if budget == 0 or not food_dict:
        return memo
    cur_food_list = get_food_list(food_dict)
    cur_food = cur_food_list[0]
    cur_food.count = budget // cur_food.cost
    if cur_food.count:
        memo.append(cur_food)
        budget -= cur_food.count * cur_food.cost
    del food_dict[cur_food.name]
    return get_food_list_by_budget_dynamic(food_dict, budget, memo)


if __name__ == "__main__":
    food_items_raw = {
    "pizza": {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog": {"cost": 30, "calories": 200},
    "pepsi": {"cost": 10, "calories": 100},
    "cola": {"cost": 15, "calories": 220},
    "potato": {"cost": 25, "calories": 350}
}

    food_items = get_food_list(food_items_raw)

    budget = 123

    foods_by_budget_greedy = get_food_list_by_budget_greedy(food_items_raw, budget)
    print(f"Список наїдків, підібраних з максимізацією калоражу в бюджеті {budget} за жадібним алгоритмом:")
    for food in foods_by_budget_greedy:
        print(food)
    print(f"Використано бюджету: {sum([food.cost * food.count for food in foods_by_budget_greedy])}")

    foods_by_budget_dynamic = get_food_list_by_budget_dynamic(food_items_raw, budget)
    print(f"Список наїдків, підібраних з максимізацією калоражу в бюджеті {budget} за динамічним алгоритмом:")
    for food in foods_by_budget_dynamic:
        print(food)
    print(f"Використано бюджету: {sum([food.cost * food.count for food in foods_by_budget_dynamic])}")