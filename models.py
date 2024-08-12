from collections import UserDict
from re import match
from datetime import datetime

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not match(r'^\d{10}$', value):
            raise ValueError('Phone number must be 10 digits')
        super().__init__(value=value)

    def __eq__(self, other):
        return isinstance(other, Phone) and self.value == other.value

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                break
        else:
            raise ValueError(f'Phone number {phone} does not belong to record {self.name}')

    def edit_phone(self, old_phone: str, new_phone: str):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                break
        else:
            raise ValueError(f'Phone number {old_phone} does not belong to record {self.name}')

    def find_phone(self, phone: str) -> Phone:
        for phone_field in self.phones:
            if phone_field.value == phone:
                return phone_field
        raise ValueError(f'Phone number {phone} does not belong to record {self.name}')

    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)

    def __str__(self):
        birthday_str = f", birthday: {self.birthday.value}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}{birthday_str}"

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[str(record.name)] = record

    def find(self, name: str) -> Record:
        if name not in self.data:
            raise ValueError('Record not found')
        return self.data[name]

    def delete(self, name: str):
        if name not in self.data:
            raise ValueError('Record not found')
        self.data.pop(name)

    def get_upcoming_birthdays(self, days=7):
        today = datetime.now().date()
        upcoming = []
        for record in self.data.values():
            if record.birthday:
                days_until_birthday = (record.birthday.value - today).days
                if 0 <= days_until_birthday <= days:
                    upcoming.append(record)
        return upcoming
