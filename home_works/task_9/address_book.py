from collections import UserDict
from datetime import datetime

from home_works.task_9.decorators import params_handler


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

class Birthday(Field):
    def __init__(self, value):
        try:
            super().__init__(datetime.strptime(value, "%d.%m.%Y"))
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")

    def __repr__(self):
        return self.value.strftime("%d.%m.%Y")


class Record:
    def __init__(self, name: str, birthday: Birthday = None, phones: list[Phone] = None):
        self.__birthday = birthday
        self.name = Name(name)
        self.phones = [] if not phones else phones

    @property
    def birthday(self):
        return str(self.__birthday)

    @property
    def days_to_birthday(self):
        tmp_bd = self.__birthday.value.replace(year=datetime.today().year)
        return (tmp_bd - datetime.today()).days

    def add_birthday(self, birthday: str):
        self.__birthday = Birthday(birthday)
        return "Birthday added successfully"


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
        return f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}, birthday: {self.birthday}"

class AddressBook(UserDict):
    command_map = {
        "add": "add_item",
        "find": "find",
        "phone": "show_phone",
        "all": "get_all",
        "remove": "remove",
        "change": "edit",
        "add-birthday": "add_birthday",
        "show-birthday": "show_birthday",
        "birthdays": "show_birthdays"
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
                self.data[name] = Record(name, phones=[Phone(phone) for phone in phones])
                return True, "Contact added successfully"
        except ValueError as ve:
            return False, "Error when add the record: " + str(ve)

    @params_handler
    def add_birthday(self, name: str, birthday: str) -> tuple:
        """Add a birthday to the contact
                Usage: add-birthday <name> <birthday in format DD.MM.YYYY>"""
        if name not in self.data:
            return False, "Contact not found"

        try:
            self.data[name].add_birthday(birthday)
            return True, "Birthday added successfully"
        except ValueError as ve:
            return False, f"Error when add the birthday: {ve}"

    @params_handler
    def find(self, name: str) -> tuple:
        """Find a contact in the address book by name
                Usage: find <name>"""
        try:
            return True, self.data.get(name)
        except KeyError:
            return False, "Contact not found"

    @params_handler
    def show_phone(self, name: str) -> tuple:
        """Find a contact in the address book by name and show his phones
                Usage: phone <name>"""
        try:
            return True, self.data.get(name).phones
        except KeyError:
            return False, "Contact not found"

    @params_handler
    def show_birthday(self, name: str) -> tuple:
        """Find a contact in the address book by name and show his birthday
                Usage: show-birthday <name>"""
        try:
            return True, str(self.data.get(name).birthday)
        except KeyError:
            return False, "Contact not found"

    @params_handler
    def show_birthdays(self):
        """Show all contacts with birthdays in the address book
                Usage: birthdays"""
        birthdays = [f"{self.data[c].name}: {self.data[c].birthday}" for c in self.data if self.data[c].days_to_birthday <= 7]

        return (True, "Next contacts have birthdays this week:\n" + "\n".join(birthdays)
        if birthdays else "No birthdays this week")

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
