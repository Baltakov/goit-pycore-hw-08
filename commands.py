from models import AddressBook, Record
from utils import save_data
from datetime import datetime, timedelta

def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    try:
        record = book.find(name)
        message = "Contact updated."
    except ValueError:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

def change_phone(args, book: AddressBook):
    name, old_phone, new_phone = args
    record = book.find(name)
    record.edit_phone(old_phone, new_phone)
    return "Phone updated."

def show_phone(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    phones = ', '.join(phone.value for phone in record.phones)
    return f"Phones for {name}: {phones}"

def show_all(book: AddressBook):
    return '\n'.join(str(record) for record in book.values())

def add_birthday(args, book: AddressBook):
    name, birthday = args
    record = book.find(name)
    record.add_birthday(birthday)
    return "Birthday added."

def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record.birthday:
        return f"Birthday for {name}: {record.birthday.value}"
    return f"No birthday for {name}."

def show_birthdays(book: AddressBook):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No birthdays coming up."
    return '\n'.join(f"{record.name.value}: {record.birthday.value}" for record in upcoming)
