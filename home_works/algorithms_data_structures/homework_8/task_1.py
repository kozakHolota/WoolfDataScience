from timeit import timeit
from typing import Dict, List


def find_coins_greedy(coins: List[int], amount: int) -> Dict[int, int]:
    coins_to_give = {}
    sorted_coins = sorted(coins, reverse=True)

    for coin in sorted_coins:
        while coin <= amount:
            if coin not in coins_to_give:
                coins_to_give[coin] = 1
            else:
                coins_to_give[coin] += 1
            amount -= coin

    return coins_to_give

def find_coins_dynamic(coins: List[int], amount: int, memo=None) -> Dict[int, int]:
    memo = memo or {}
    if not amount:
        return memo

    sorted_coins = sorted(coins, reverse=True)
    current_coin = sorted_coins[0]
    amount_to_give = amount // current_coin
    if amount_to_give:
        memo[current_coin] = amount_to_give
    amount -= current_coin * amount_to_give
    sorted_coins.remove(current_coin)
    return find_coins_dynamic(sorted_coins, amount, memo)

if __name__ == "__main__":
    coins = [50, 25, 10, 5, 2, 1]
    amount = 113
    print(f"Сума, необхідна дя видачі: {amount}")
    print(f"Номінали монет: {coins}")
    print(f"Підраховуємо необхідну кількість монет за жадібним алгоритмом: " + str(find_coins_greedy(coins, amount)))
    print(f"Підраховуємо необхідну кількість монет за алгоритмом динамічного програмування: " + str(find_coins_dynamic(coins, amount)))

    greedy_alg_result = timeit(lambda: find_coins_greedy(coins, amount))
    dynamic_alg_result = timeit(lambda: find_coins_dynamic(coins, amount))

    winner_time = greedy_alg_result if greedy_alg_result < dynamic_alg_result else dynamic_alg_result
    looser_time = greedy_alg_result if winner_time == dynamic_alg_result else dynamic_alg_result
    winner_alg = "жадібний алгоритм" if greedy_alg_result < dynamic_alg_result else "динамічний алгоритм"

    print(f"Ефективнішим алгоритмом є {winner_alg} з часом виконання: {winner_time}. Час виконання конкурента: {looser_time}")