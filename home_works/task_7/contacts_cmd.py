import re
from typing import List
import cmdlets
from home_works.task_7.cmd_io import output_error, get_input, output_info


def parse_input(input_string: str) -> List[str]:
    return re.split(r"\s+", input_string)

def execute_command(command: str) -> None:
    command_args = parse_input(command)
    _command = command_args[0].lower()
    arguments = command_args[1:] if len(command_args) > 1 else []

    try:
        if arguments and (arguments[0] == "help" or arguments[0] == "h" or arguments[0] == "?"):
            output_info(getattr(cmdlets, _command).__doc__)
            return
        getattr(cmdlets, _command)(*arguments)
    except AttributeError:
        output_error(f"Command '{_command}' not found")
    except Exception as e:
        output_error(f"Command '{command}' crashed with error: {e}")
        output_info("Command help")
        output_info(getattr(cmdlets, _command).__doc__)

def command_handler() -> None:
    prompt = "Contacts CMD> "
    output_info("Welcome to Contacts CMD")
    output_info("Type 'help' to get whole list of commands")

    while True:
        command = get_input(prompt)
        execute_command(command)

def main() -> None:
    command_handler()


if __name__ == "__main__":
    main()
