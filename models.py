"""Contact fields, records and address book."""
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


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

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
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones = "; ".join(str(phone) for phone in self.phones)
        result = f"Contact name: {self.name.value}, phones: {phones}"
        if self.birthday is not None:
            result += f", birthday: {self.birthday.value.strftime('%d.%m.%Y')}"
        return result


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        self.data.pop(name, None)

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

                upcoming.append({
                    "name": record.name.value,
                    "congratulation_date": next_birthday.strftime("%d.%m.%Y")
                })

        return upcoming

