"""Command handlers for contacts and birthdays."""
from colorama import Fore
from models import Record
from utils import input_error


@input_error
def add_contact(args, book):
    if len(args) < 2:
        raise ValueError(Fore.RED + "Usage: add [name] [phone]")

    name = " ".join(args[:-1])
    phone = args[-1]

    record = book.find(name)

    if record is None:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return Fore.GREEN + "Contact added."

    record.add_phone(phone)
    return Fore.GREEN + "Contact updated."


@input_error
def change_contact(args, book):
    if len(args) < 3:
        raise ValueError(Fore.RED + "Usage: change [name] [old phone] [new phone]")

    name = " ".join(args[:-2])
    old_phone = args[-2]
    new_phone = args[-1]

    record = book.find(name)
    if record is None:
        raise ValueError(Fore.MAGENTA + f"Contact '{name}' not found.")

    record.edit_phone(old_phone, new_phone)
    return Fore.GREEN + "Contact updated."


@input_error
def show_phone(args, book):
    if not args:
        raise ValueError(Fore.RED + "Usage: phone [name]")

    name = " ".join(args)
    record = book.find(name)

    if record is None:
        raise ValueError(Fore.MAGENTA + f"Contact '{name}' not found.")

    return (Fore.GREEN + "; ".join(str(phone) for phone in record.phones)
            or Fore.YELLOW + "No phone numbers saved.")


@input_error
def show_all(args, book):
    if args:
        raise ValueError(Fore.RED + "Usage: all")
    if not book.data:
        return Fore.GREEN + "Address book is empty."
    return "\n".join(str(record) for record in book.data.values())


@input_error
def add_birthday(args, book):
    if len(args) < 2:
        raise ValueError(Fore.RED + "Usage: add-birthday [name] [DD.MM.YYYY]")

    name = " ".join(args[:-1])
    birthday = args[-1]

    record = book.find(name)
    if record is None:
        raise ValueError(Fore.MAGENTA + f"Contact '{name}' not found.")

    record.add_birthday(birthday)
    return Fore.GREEN + "Birthday added."


@input_error
def show_birthday(args, book):
    if not args:
        raise ValueError(Fore.RED + "Usage: show-birthday [name]")

    name = " ".join(args)
    record = book.find(name)
    if record is None:
        raise ValueError(Fore.MAGENTA + f"Contact '{name}' not found.")
    if record.birthday is None:
        return Fore.YELLOW + "Birthday not set."

    return record.birthday.value.strftime("%d.%m.%Y")


@input_error
def birthdays(args, book):
    if len(args) != 1:
        raise ValueError("Usage: birthdays [number_of_days]")

    try:
        days = int(args[0])
    except ValueError:
        raise ValueError("The number of days must be an integer.")

    upcoming = book.get_upcoming_birthdays(days)

    if not upcoming:
        return Fore.GREEN + f"No birthdays in the next {days} days."

    return "\n".join(
        f"{person['name']}: {person['congratulation_date']}"
        for person in upcoming
    )

@input_error
def search_contacts(args, book):
    if not args:
        raise ValueError(Fore.RED + "Usage: search [name, phone or email]")

    query = " ".join(args)
    results = book.search(query)

    if not results:
        return Fore.YELLOW + "No contacts found."

    return "\n".join(str(record) for record in results)
