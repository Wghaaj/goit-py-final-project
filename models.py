"""Contact fields, records and address book."""

import re
from collections import UserDict
from datetime import date, datetime, timedelta


# Contact fields and validation

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

            # Ensure the date strictly follows DD.MM.YYYY.
            if birthday.strftime("%d.%m.%Y") != value:
                raise ValueError

            super().__init__(birthday)

        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Email(Field):
    EMAIL_PATTERN = re.compile(
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    )

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
    """Store and manage an individual contact."""

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.email = None
        self.address = None

    def edit_name(self, new_name):
        if self.name is None:
            raise ValueError("Contact not found.")

        self.name = Name(new_name)

    # Phone management

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

    # Birthday management

    def add_birthday(self, birthday):
        if self.birthday is not None:
            raise ValueError("Birthday already set.")

        self.birthday = Birthday(birthday)

    def remove_birthday(self):
        if self.birthday is None:
            raise ValueError("Birthday not set.")

        self.birthday = None

    def edit_birthday(self, new_birthday):
        if self.birthday is None:
            raise ValueError("Birthday not set.")

        self.birthday = Birthday(new_birthday)

    # Email management

    def add_email(self, email):
        if self.email is not None:
            raise ValueError("Email already set.")

        self.email = Email(email)

    def remove_email(self):
        if self.email is None:
            raise ValueError("Email not set.")

        self.email = None

    def edit_email(self, new_email):
        if self.email is None:
            raise ValueError("Email not set.")

        self.email = Email(new_email)

    # Address management

    def add_address(self, address):
        if self.address is not None:
            raise ValueError("Address already set.")

        self.address = Address(address)

    def remove_address(self):
        if self.address is None:
            raise ValueError("Address not set.")

        self.address = None

    def edit_address(self, new_address):
        if self.address is None:
            raise ValueError("Address not set.")

        self.address = Address(new_address)

    def __str__(self):
        phones = "; ".join(str(phone) for phone in self.phones)
        result = f"Contact name: {self.name.value}, phones: {phones}"

        # Include optional fields only when they are available.
        if self.birthday is not None:
            result += f", birthday: {self.birthday.value.strftime('%d.%m.%Y')}"

        if self.email is not None:
            result += f", email: {self.email.value}"

        if self.address is not None:
            result += f", address: {self.address.value}"

        return result


class AddressBook(UserDict):
    """Manage the collection of contacts."""

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

        # Update both the contact name and its dictionary key.
        record.edit_name(new_name)
        del self.data[old_name]
        self.data[new_name] = record

    def search(self, query):
        """Search contacts by name, phone number or email."""
        query = query.strip().lower()
        results = []

        if not query:
            return results

        for record in self.values():
            email = getattr(record, "email", None)

            # Check all searchable fields without duplicating results.
            if (
                query in record.name.value.lower()
                or any(query in phone.value for phone in record.phones)
                or (email and query in email.value.lower())
            ):
                results.append(record)

        return results

    @staticmethod
    def birthday_in_year(birthday, year):
        """Handle birthdays on 29 February in non-leap years."""
        try:
            return birthday.replace(year=year)
        except ValueError:
            return birthday.replace(year=year, day=28)

    def get_upcoming_birthdays(self, days=7):
        if (
            not isinstance(days, int)
            or isinstance(days, bool)
            or not 1 <= days <= 365
        ):
            raise ValueError(
                "The search period must be from 1 to 365 days."
            )

        today = date.today()
        upcoming = []

        for record in self.values():
            if record.birthday is None:
                continue

            birthday = record.birthday.value.date()

            # Find the next occurrence of the contact's birthday.
            next_birthday = self.birthday_in_year(birthday, today.year)

            if next_birthday < today:
                next_birthday = self.birthday_in_year(
                    birthday, today.year + 1
                )

            days_until = (next_birthday - today).days

            if 0 <= days_until <= days:
                congratulation_date = next_birthday

                # Move weekend congratulations to Monday.
                if congratulation_date.weekday() >= 5:
                    congratulation_date += timedelta(
                        days=7 - congratulation_date.weekday()
                    )

                upcoming.append({
                    "name": record.name.value,
                    "congratulation_date": congratulation_date.strftime(
                        "%d.%m.%Y"
                    ),
                })

        # Sort results chronologically.
        upcoming.sort(
            key=lambda person: datetime.strptime(
                person["congratulation_date"], "%d.%m.%Y"
            )
        )

        return upcoming