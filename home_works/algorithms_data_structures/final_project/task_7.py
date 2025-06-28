import random


def dice_throw_monte_carlo(experiments: int):
    scores = {k: 0 for k in range(2, 13)}
    scores_probability = {}
    for _ in range(experiments):
        score = random.randint(2, 12)
        scores[score] += 1

    for score in scores:
        scores_probability[score] = (scores[score] / experiments) * 100

    return scores_probability

def print_results(probability_dict: dict, experiments: int):
    print("-" * 20)
    print(f"Вірогідності випадання очків на {experiments} експериментів")
    print("-"*20)
    for score in probability_dict:
        print(f"{score}: {probability_dict[score]}%")

if __name__ == "__main__":
    for experiments in [1000, 10000, 100000, 500000]:
        scores_probability = dice_throw_monte_carlo(experiments)
        print_results(scores_probability, experiments=experiments)
