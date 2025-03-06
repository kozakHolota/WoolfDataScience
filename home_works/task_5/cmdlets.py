import sys

from home_works.task_5.cmd_io import _output_info, _get_input, _deinit_colorama, _output_error

_contacts: dict = {}

def hello() -> None:
    """Prints a welcome message.
    Usage: hello"""
    _output_info("How can I help you?")

def exit() -> None:
    """Exits the program.
    Usage: exit"""
    acceptance = _get_input("Are you sure? (y/n) ")
    if acceptance == "y":
        _output_info("Goodbye!")
        _deinit_colorama()
        sys.exit(0)
    elif acceptance == "n":
        _output_info("Okay, continue work.")
        return
    else:
        _output_error("Wrong input. Please, try again.")
        exit()

def all() -> None:
    """Prints all contacts.
    Usage: all"""
    for contact in _contacts.values():
        _output_info(f"{contact['name']}: {contact['phone']}")

def phone(name: str) -> None:
    """Prints a phone number of a contact.
    Usage: phone <name>"""
    if name in _contacts:
        _output_info(_contacts[name]['phone'])
    else:
        _output_error(f"Contact with name {name} not found.")

def add(name: str, phone: str) -> None:
    """Adds a new contact.
    Usage: add <name> <phone>"""
    _contacts[name] = {'name': name, 'phone': phone}
    _output_info(f"Contact {name} added.")

def change(name: str, phone: str) -> None:
    """Changes a phone number of a contact.
    Usage: change <name> <phone>"""
    if name in _contacts:
        _contacts[name]['phone'] = phone
        _output_info(f"Contact {name} phone number changed.")
    else:
        _output_error(f"Contact with name {name} not found.")

def remove(name: str) -> None:
    """Removes a contact.
    Usage: remove <name>"""
    if name in _contacts:
        del _contacts[name]
        _output_info(f"Contact {name} removed.")
    else:
        _output_error(f"Contact with name {name} not found.")

def quit() -> None:
    """Exits the program.
    Usage: quit"""
    exit()

def close() -> None:
    """Exits the program.
    Usage: close"""
    exit()

def help()->None:
    """Prints a list of available commands.
    Usage: help"""
    _output_info(f"Available commands: {', '.join([f for f in dir(sys.modules[__name__]) if not f.startswith('_') and f not in sys.modules])}")
    _output_info("If you want to get help on some command, type: command help")