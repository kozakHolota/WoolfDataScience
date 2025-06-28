from pulp import LpVariable, LpProblem, value, LpMaximize


def juice_factory(water_max: int, juice_max: int, fruit_pure_max: int, sugar_max: int):
    water = LpVariable("water", 0, water_max)
    juice = LpVariable("juice", 0, juice_max)
    fruit_pure = LpVariable("fruit_pure", 0, fruit_pure_max)
    sugar = LpVariable("sugar", 0, sugar_max)
    juice_factory_problem = LpProblem("juiceOptimizationProblem", LpMaximize)
    juice_factory_problem += 2*water + sugar + juice
    juice_factory_problem += 2*fruit_pure + water

    juice_factory_problem.solve()

    return {
        "Вода": value(water),
        "Лимонний сік": value(juice),
        "Фруктове пюре": value(fruit_pure),
        "Цукор": value(sugar)
    }

if __name__ == "__main__":
    water_max = 100
    sugar_max = 50
    fruit_pure_max = 40
    juice_max = 30
    ingridients = juice_factory(water_max, juice_max, fruit_pure_max, sugar_max)
    print("Для максимізації прибутку ми використовуємо такі ресурси: ")
    for ingridient in ingridients:
        if ingridients[ingridient]:
            print(f"{ingridient}: {ingridients[ingridient]}")
