import re
import sys
from io import StringIO

from home_works.task_7.cmd_io import output_info, get_input, deinit_colorama, output_error, bot_command

_contacts: dict = {}

@bot_command
def exit() -> None:
    """Exits the program.
    Usage: exit"""
    acceptance = get_input("Are you sure? (y/n) ")
    if acceptance == "y":
        output_info("Goodbye!")
        deinit_colorama()
        sys.exit(0)
    elif acceptance == "n":
        output_info("Okay, continue work.")
        return
    else:
        output_error("Wrong input. Please, try again.")
        exit()

def quit() -> None:
    """Exits the program.
    Usage: quit"""
    exit()

def close() -> None:
    """Exits the program.
    Usage: close"""
    exit()

@bot_command
def hello() -> tuple[bool, str]:
    """Prints a welcome message.
    Usage: hello"""
    return True, "How can I help you?"

@bot_command
def all() -> tuple[bool, str]:
    """Prints all contacts.
    Usage: all"""

    contacts = StringIO()
    for contact in _contacts.values():
        contacts.write(f"{contact['name']}: {contact['phone']}\n")

    return True, contacts.getvalue()

@bot_command
def phone(name: str) -> tuple[bool, str]:
    """Prints a phone number of a contact.
    Usage: phone <name>"""
    if name in _contacts:
        return True, _contacts[name]['phone']
    else:
        return False, f"Contact with name {name} not found."

@bot_command
def add(name: str, phone: str) -> tuple[bool, str]:
    """Adds a new contact.
    Usage: add <name> <phone>"""
    _contacts[name] = {'name': name, 'phone': phone}
    return True, f"Contact {name} added."

@bot_command
def change(name: str, phone: str) -> tuple[bool, str]:
    """Changes a phone number of a contact.
    Usage: change <name> <phone>"""
    if name in _contacts:
        _contacts[name]['phone'] = phone
        return True, f"Contact {name} phone number changed."
    else:
        return False, f"Contact with name {name} not found."

@bot_command
def remove(name: str) -> tuple[bool, str]:
    """Removes a contact.
    Usage: remove <name>"""
    if name in _contacts:
        del _contacts[name]
        return True, f"Contact {name} removed."
    else:
        return  False, f"Contact with name {name} not found."

@bot_command
def help()->tuple[bool, str]:
    """Prints a list of available commands.
    Usage: help"""
    return True, (f"Available commands: {', '.join([f for f in globals() if re.match(r"\b[a-z]+\b", f) and f not in sys.modules])}\n"
            f"If you want to get help on some command, type: command help")