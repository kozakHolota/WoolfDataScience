from collections import deque
from random_word import RandomWords

def is_palindrome(string: str):
    dq = deque()
    string = string.lower().replace(" ", "")
    for char in string:
        dq.append(char)
    while len(dq) > 1:
        if dq.popleft() != dq.pop():
            return False
    return True

if __name__ == "__main__":
    rw = RandomWords()
    while True:
        word = rw.get_random_word()
        ip = is_palindrome(word)
        print(f"{word}: {ip}")
        if ip:
            print(f"Found palindrome: {word}")
            break