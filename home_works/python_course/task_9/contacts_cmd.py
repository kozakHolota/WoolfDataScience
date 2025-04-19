from home_works.python_course.task_9.command_handler import CommandHandler


def main():
    prompt = "Contacts CMD> "
    cmd_handler = CommandHandler(prompt)
    cmd_handler.interpreter_loop()

if __name__ == "__main__":
    main()