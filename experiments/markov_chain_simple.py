import numpy as np

from home_works.numerical_programming.util import coroutine


@coroutine
def markov_chain(transition_prob: dict):
    states = list(transition_prob.keys())
    current_state = None
    while True:
        if current_state is None:
            state = np.random.choice(states)
        else:
            if current_state not in states:
                raise ValueError(f"State {current_state} is not in states {states}")
            state = np.random.choice(
                states,
                p=[transition_prob[current_state][next_state] for next_state in states],
            )
        # Повертаємо наступний стан назовні і одночасно приймаємо вхідний на наступну ітерацію
        current_state = (yield str(state))


def generate_states(transition_prob: dict, n: int):
    mc = markov_chain(transition_prob)
    current_state = mc.send(None)
    states = []
    for _ in range(n):
        current_state = mc.send(current_state)
        states.append(current_state)

    return states


if __name__ == "__main__":
    transition_prob = {
        "Sunny": {"Sunny": 0.8, "Rainy": 0.19, "Snowy": 0.01},
        "Rainy": {"Sunny": 0.2, "Rainy": 0.7, "Snowy": 0.1},
        "Snowy": {"Sunny": 0.1, "Rainy": 0.2, "Snowy": 0.7},
    }

    n = int(input("How many states to generate? "))
    print(generate_states(transition_prob, n))
