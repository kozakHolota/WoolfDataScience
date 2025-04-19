import sys
from typing import Collection

from colorama import Fore, Style, deinit

from home_works.python_course.task_8.address_book import AddressBook
from home_works.python_course.task_8.decorators import params_handler


class CommandHandler:
    command_map = {
        "help": "help",
    }
    def __init__(self, prompt: str):
        self.prompt = prompt
        self.libs = [AddressBook(), self]

    def __get_input(self, prompt: str) -> str:
        return input(Fore.BLUE + prompt + Style.DIM + Style.RESET_ALL)

    def __output_info(self, msg: str) -> None:
        print(Fore.GREEN + str(msg) + Style.DIM + Style.RESET_ALL)

    def __output_error(self, msg: str) -> None:
        print(Fore.RED + str(msg) + Style.DIM + Style.RESET_ALL)


    def __exit(self) -> None:
        """Exits interpreter
                        Usage: exit"""
        acceptance = self.__get_input("Are you sure? (y/n) ")
        if acceptance == "y":
            self.__output_info("Goodbye!")
            deinit()
            sys.exit(0)
        elif acceptance == "n":
            self.__output_info("Okay, continue work.")
            return
        else:
            self.__output_error("Wrong input. Please, try again.")
            exit()

    @params_handler
    def help(self):
        """Displays all available commands
                            Usage: help"""
        commands = ["exit"]
        for lib in self.libs:
            for command in lib.command_map:
                commands.append(command)

        return True, f"Available commands: {', '.join(commands)}"

    def __handle_command(self, command: str):
        command_list = command.split(' ')
        command_name = command_list[0].lower()
        command_args = command_list[1:] if len(command_list) > 1 else []

        if command_name == "exit":
            try:
                self.__exit()
            except (TypeError, ValueError) as e:
                self.__output_error(f"Incorrect arguments to the command:\n{self.__exit.__doc__}")
        else:
            for lib in self.libs:
                if command_name in lib.command_map:
                    if command_args and command_args[0] in ["help", "h", "?"]:
                        self.__output_info(getattr(lib, lib.command_map[command_name]).__doc__)
                        return
                    result, output = getattr(lib, lib.command_map[command_name])(*command_args)
                    if result:
                        if isinstance(output, Collection) and not isinstance(output, str):
                            for line in output:
                                self.__output_info(line)
                        self.__output_info(output)
                        return
                    else:
                        self.__output_error(output)
                        return
            self.__output_error(f"Command {command_name} not found.")

    def interpreter_loop(self):
        self.__output_info("Welcome to Contacts CMD")
        self.__output_info("Type 'help' to get whole list of commands")
        while True:
            command = self.__get_input(self.prompt)
            self.__handle_command(command)

