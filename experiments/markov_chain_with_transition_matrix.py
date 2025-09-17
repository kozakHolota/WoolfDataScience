from typing import List

import numpy as np

from home_works.numerical_programming.util import coroutine


@coroutine
def markov_chain(transition_matrix: List[List[float]], states: List[str]):
    transition_matrix = np.atleast_2d(transition_matrix)
    index_dict = {states[index]: index for index in range(len(states))}
    current_state = None
    while True:
        if current_state is None:
            state = np.random.choice(states)
        else:
            state = np.random.choice(
                states,
                p=transition_matrix[index_dict[current_state], :]
            )
        # Повертаємо наступний стан і одночасно приймаємо вхідний на наступну ітерацію
        current_state = (yield str(state))


def generate_states(transition_matrix: List[List[float]], states: List[str], n: int):
    mc = markov_chain(transition_matrix, states)
    current_state = mc.send(None)
    states = []
    for _ in range(n):
        current_state = mc.send(current_state)
        states.append(current_state)

    return states

if __name__ == "__main__":
    transition_matrix = [[0.8, 0.19, 0.01],
                         [0.2, 0.7, 0.1],
                         [0.1, 0.2, 0.7]]
    states = ['Sunny', 'Rainy', 'Snowy']

    n  = int(input("How many states to generate? "))
    print(generate_states(transition_matrix, states, n))
