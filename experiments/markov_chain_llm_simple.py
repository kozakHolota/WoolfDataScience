import random
import re
from pathlib import Path

import nltk
from nltk import word_tokenize

from experiments.markov_chain_simple import generate_states
from home_works.numerical_programming.util import coroutine

nltk.download('punkt')
nltk.download('punkt_tab')

def read_all_stories():
    sherlock_dir = Path(__file__).parent / "data" / "sherlock"
    stories = []
    for story in sherlock_dir.iterdir():
        with story.open("r") as story_file:
            for line in story_file:
                line = line.strip()
                if line == '----------':
                    break
                if line:
                    stories.append(line)

    return stories

def clean_stories(stories: list):
    cleaned_stories = []
    for line in stories:
        line = line.lower()
        line = re.sub(r"[,.\"\'!@#$%^&*(){}?/;`~:<>+=-\\]", "", line)
        tokens = word_tokenize(line)
        words = [word for word in tokens if word.isalpha()]
        cleaned_stories += words

    return cleaned_stories

def make_markov_model(cleaned_stories, n_gram=2):
    markov_model = {}
    for i in range(len(cleaned_stories)-n_gram-1):
        curr_state, next_state = "", ""
        for j in range(n_gram):
            curr_state += cleaned_stories[i+j] + " "
            next_state += cleaned_stories[i+j+n_gram] + " "
        curr_state = curr_state[:-1]
        next_state = next_state[:-1]
        if curr_state not in markov_model:
            markov_model[curr_state] = {}
            markov_model[curr_state][next_state] = 1
        else:
            if next_state in markov_model[curr_state]:
                markov_model[curr_state][next_state] += 1
            else:
                markov_model[curr_state][next_state] = 1

    # calculating transition probabilities
    for curr_state, transition in markov_model.items():
        total = sum(transition.values())
        for state, count in transition.items():
            markov_model[curr_state][state] = count/total

    return markov_model

@coroutine
def generate_story(markov_model):
    # Чекаємо перший запит (start, limit)
    start, limit = (yield)
    while True:
        story_tokens = []
        curr_state = start

        for _ in range(limit):
            if curr_state not in markov_model:
                break
            next_state = start + " " + random.choices(
                list(markov_model[curr_state].keys()),
                list(markov_model[curr_state].values())
            )[0]
            story_tokens.append(next_state)
            curr_state = next_state

        story = " ".join(story_tokens)
        # Віддаємо історію і одночасно приймаємо наступні (start, limit)
        start, limit = (yield story)


if __name__ == "__main__":
    col = read_all_stories()
    print(len(col))
    all_words = clean_stories(col)
    print(len(all_words))
    markov_model = make_markov_model(all_words)
    print("Number of states: ", len(markov_model))
    print(tuple(markov_model.items())[:3])
    n = int(input("How many states to generate? "))
    stories_n = int(input("How many stories? "))
    start = input("Enter starting phrase: ")
    story_generator = generate_story(markov_model)

    for _ in range(stories_n):
        print(story_generator.send((start, n)))
