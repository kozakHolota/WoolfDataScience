from collections import deque


def are_brackets_symmetric(code_line: str) -> bool:
    open_brackets_stack = deque()
    open_brackets = {"}": "{", ")": "("}
    for char in code_line:
        if char in open_brackets.values():
            open_brackets_stack.append(char)
        elif char in open_brackets.keys():
            if not open_brackets_stack or open_brackets[char] != open_brackets_stack.pop():
                return False
    return not open_brackets_stack

if __name__ == "__main__":
    while True:
        code_line = input("Enter code line: ")
        if not code_line:
            break
        print("Code block is symmetric") if are_brackets_symmetric(code_line) \
            else print("Code block is not symmetric")