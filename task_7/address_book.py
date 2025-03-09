from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

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
    def __setitem__(self, key, value):
        if not isinstance(value, Record):
            raise ValueError("Value must be an instance of class Record")

        self.data[key] = value


