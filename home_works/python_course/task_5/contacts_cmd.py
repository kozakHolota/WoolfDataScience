import re
from typing import List
import cmdlets
from home_works.python_course.task_5.cmd_io import _output_error, _get_input, _output_info


def parse_input(input_string: str) -> List[str]:
    return re.split(r"\s+", input_string)

def execute_command(command: str) -> None:
    command_args = parse_input(command)
    _command = command_args[0].lower()
    arguments = command_args[1:] if len(command_args) > 1 else []

    try:
        if arguments and (arguments[0] == "help" or arguments[0] == "h" or arguments[0] == "?"):
            _output_info(getattr(cmdlets, _command).__doc__)
            return
        getattr(cmdlets, _command)(*arguments)
    except AttributeError:
        _output_error(f"Command '{_command}' not found")
    except Exception as e:
        _output_error(f"Command '{command}' crashed with error: {e}")
        _output_info("Command help")
        _output_info(getattr(cmdlets, _command).__doc__)

def command_handler() -> None:
    prompt = "Contacts CMD> "
    _output_info("Welcome to Contacts CMD")
    _output_info("Type 'help' to get whole list of commands")

    while True:
        command = _get_input(prompt)
        execute_command(command)

def main() -> None:
    command_handler()


if __name__ == "__main__":
    main()
