from typing import List


def float_binary_search(arr: List[float], value: float, iterations: int = 0, greater_neibor=None) -> tuple[int, float] | tuple[
    int, float | int, None] | None | tuple[int, None]:
    half_len = len(arr) // 2

    if len(arr) == 1:
        iterations += 1
        if value == arr[0]:
            greater_neibor = value if not greater_neibor else greater_neibor
        else:
            greater_neibor = None
    else:
        iterations += 1
        if value < arr[half_len]:
            return float_binary_search(arr[:half_len], value, iterations=iterations, greater_neibor=arr[half_len])
        elif value > arr[half_len]:
            return float_binary_search(arr[half_len:], value, iterations=iterations, greater_neibor=arr[half_len + 1])
        else:
            try:
                greater_neibor = arr[half_len + 1]
            except IndexError:
               greater_neibor = value

    return iterations, greater_neibor


def print_result(value: float, result: tuple[int, float] | tuple[
    int, float | int, None] | None | tuple[int, None]):
    iterations, neighbar = result
    print(f"Елемент {value} знайдено за {iterations} ітерацій. Найбільше сусіднє значення: {neighbar}") if neighbar \
        else print(f"Елемент {value} не знайдено. Пройдено {iterations} ітерацій")

if __name__ == "__main__":
    arr = sorted([1/3, 2/4, 3/4, 4/3, 5/2, 6/4, 7/2, 8/7, 9/6, 10/3])
    print(arr)

    item_to_search1 = 6/4
    res1 = float_binary_search(arr, item_to_search1)
    print_result(item_to_search1, res1)

    item_to_search2 = 3/4
    res2 = float_binary_search(arr, item_to_search2)
    print_result(item_to_search2, res2)

    item_to_search3 = 8/7
    res3 = float_binary_search(arr, item_to_search3)
    print_result(item_to_search3, res3)

    item_to_search4 = 1/3
    res4 = float_binary_search(arr, item_to_search4)
    print_result(item_to_search4, res4)

    item_to_search5 = 3.1415956
    res5 = float_binary_search(arr, item_to_search5)
    print_result(item_to_search5, res5)