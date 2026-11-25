"""Contact fields, records and address book."""

import re
from collections import UserDict
from datetime import date, datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if len(value) != 10 or not value.isascii() or not value.isdigit():
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            birthday = datetime.strptime(value, "%d.%m.%Y")
            if birthday.strftime("%d.%m.%Y") != value:
                raise ValueError
            super().__init__(birthday)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Email(Field):
    EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

    def __init__(self, value):
        if isinstance(value, str):
            value = value.strip()
        if not isinstance(value, str) or not self.EMAIL_PATTERN.fullmatch(value):
            raise ValueError("Invalid email format.")
        super().__init__(value)


class Address(Field):
    def __init__(self, value):
        if isinstance(value, str):
            value = value.strip()
        if not isinstance(value, str) or not value:
            raise ValueError("Address cannot be empty.")
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.email = None
        self.address = None

    def edit_name(self, new_name):
        if self.name is not None:
            self.name = Name(new_name)
        else:
            raise ValueError("Contact not found")

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        found_phone = self.find_phone(phone)
        if found_phone is not None:
            self.phones.remove(found_phone)

    def edit_phone(self, old_phone, new_phone):
        found_phone = self.find_phone(old_phone)
        if found_phone is None:
            raise ValueError("Phone number not found.")
        found_phone.value = Phone(new_phone).value

    def find_phone(self, phone):
        for saved_phone in self.phones:
            if saved_phone.value == phone:
                return saved_phone
        return None

    def add_birthday(self, birthday):
        if self.birthday is not None:
            raise ValueError("Birthday already set.")
        self.birthday = Birthday(birthday)

    def remove_birthday(self):
        if self.birthday is not None:
            self.birthday = None
        else:
            raise ValueError("Birthday not set.")

    def edit_birthday(self, new_birthday):
        if self.birthday is not None:
            self.birthday = Birthday(new_birthday)
        else:
            raise ValueError("Birthday not set.")

    def add_email(self, email):
        if self.email is not None:
            raise ValueError("Email already set.")
        self.email = Email(email)

    def remove_email(self):
        if self.email is not None:
            self.email = None
        else:
            raise ValueError("Email not set.")

    def edit_email(self, new_email):
        if self.email is not None:
            self.email = Email(new_email)
        else:
            raise ValueError("Email not set.")

    def add_address(self, address):
        if self.address is not None:
            raise ValueError("Address already set.")
        self.address = Address(address)

    def remove_address(self):
        if self.address is not None:
            self.address = None
        else:
            raise ValueError("Address not set.")

    def edit_address(self, new_address):
        if self.address is not None:
            self.address = Address(new_address)
        else:
            raise ValueError("Address not set.")

    def __str__(self):
        phones = "; ".join(str(phone) for phone in self.phones)
        result = f"Contact name: {self.name.value}, phones: {phones}"
        if self.birthday is not None:
            result += f", birthday: {self.birthday.value.strftime('%d.%m.%Y')}"
        if self.email is not None:
            result += f", email: {self.email.value}"
        if self.address is not None:
            result += f", address: {self.address.value}"
        return result


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        self.data.pop(name, None)

    def edit_name(self, old_name: str, new_name: str):
        record = self.find(old_name)
        if record is None:
            raise KeyError(f"Contact '{old_name}' not found.")
        if old_name == new_name:
            return
        if self.find(new_name) is not None:
            raise ValueError(f"Contact '{new_name}' already exists.")

        record.edit_name(new_name)
        del self.data[old_name]
        self.data[record.name.value] = record

    def get_upcoming_birthdays(self):
        today = date.today()
        upcoming = []

        for record in self.data.values():
            if record.birthday is None:
                continue

            birthday = record.birthday.value.date()
            try:
                next_birthday = birthday.replace(year=today.year)
            except ValueError:
                next_birthday = birthday.replace(year=today.year, day=28)

            if next_birthday < today:
                try:
                    next_birthday = birthday.replace(year=today.year + 1)
                except ValueError:
                    next_birthday = birthday.replace(year=today.year + 1, day=28)

            if 0 <= (next_birthday - today).days <= 7:
                if next_birthday.weekday() >= 5:
                    next_birthday += timedelta(days=7 - next_birthday.weekday())

                upcoming.append(
                    {
                        "name": record.name.value,
                        "congratulation_date": next_birthday.strftime("%d.%m.%Y"),
                    }
                )

        return upcoming
