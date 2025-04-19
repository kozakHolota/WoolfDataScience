from pathlib import Path

import click

from home_works.python_course.task_10.command_handler import CommandHandler

@click.command()
@click.option("--contacts-path", default="contacts.pkl", help="Path to contacts file")
def main(contacts_path:str):
    prompt = "Contacts CMD> "
    cmd_handler = CommandHandler(prompt, Path(contacts_path))
    cmd_handler.interpreter_loop()

if __name__ == "__main__":
    main()