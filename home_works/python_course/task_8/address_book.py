from collections import UserDict
from home_works.python_course.task_8.decorators import params_handler


class Field:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value: str):
        if len(value) != 10:
            raise ValueError("Phone number must be 10 digits")
        super().__init__(value)


class Record:
    def __init__(self, name: str, phones: list[Phone] = None):
        self.name = Name(name)
        self.phones = [] if not phones else phones

    def add_phone(self, phone: str):
        try:
            self.phones.append(Phone(phone))
            return "Phone added successfully"
        except ValueError as ve:
            return str(ve)

    def remove_phone(self, phone: str):
        try:
            self.phones.remove(Phone(phone))
            return "Phone removed successfully"
        except ValueError:
            return "Phone not found"

    def edit_phone(self, old_phone: str, new_phone: str):
        try:
            self.phones[self.phones.index(Phone(old_phone))] = Phone(new_phone)
            return "Phone edited successfully"
        except ValueError:
            return "Phone not found"

    def is_phone_present(self, phone: str):
        return Phone(phone) in self.phones

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}"

class AddressBook(UserDict):
    command_map = {
        "add": "add_item",
        "find": "find",
        "all": "get_all",
        "remove": "remove",
        "edit": "edit",
    }
    def __setitem__(self, key, value):
        if not isinstance(value, Record):
            raise ValueError("Value must be an instance of class Record")

        self.data[key] = value

    @params_handler
    def add_item(self, name: str, *phones) -> tuple:
        """Add a new contact to the address book
                Usage: add <name> <phone> [<phone>] [<phone>] ..."""
        if not phones:
            return False, "No phones provided. At least one must be present."

        try:
            if name in self.data:
                for phone in phones:
                    self.data[name].add_phone(phone)
                return True, "Contact updated successfully"
            else:
                self.data[name] = Record(name, [Phone(phone) for phone in phones])
                return True, "Contact added successfully"
        except ValueError as ve:
            return False, "Error when add the record: " + str(ve)

    @params_handler
    def find(self, name: str) -> tuple:
        """Find a contact in the address book by name
                Usage: find <name>"""
        try:
            return True, self.data.get(name)
        except KeyError:
            return False, "Contact not found"

    @params_handler
    def get_all(self) -> tuple:
        """List all contacts in the address book
                Usage: all"""
        return True, list(self.data.values())

    @params_handler
    def remove(self, name: str) -> tuple:
        """Remove a contact from the address book by name
                Usage: remove <name>"""
        try:
            del self.data[name]
            return True, "Contact removed successfully"
        except KeyError:
            return False, "Contact not found"

    @params_handler
    def edit(self, name: str, phone: str, new_phone: str) -> tuple:
        """Edit a phone number of a contact in the address book by name
                Usage: edit <name> <phone> <new_phone>"""
        try:
            self.data[name].edit_phone(phone, new_phone)
            return True, "Phone edited successfully"
        except ValueError:
            return False, "Phone not found"
