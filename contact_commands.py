"""Command handlers for contacts and birthdays."""

from colorama import Fore
from models import Record
from utils import input_error


@input_error
def change_name(args, book):
    if len(args) != 2:
        raise ValueError(Fore.RED + "Usage: change-name [old_name] [new_name]")

    old_name, new_name = args
    record = book.find(old_name)
    if record is None:
        raise ValueError(Fore.MAGENTA + f"Contact '{old_name}' not found.")
    book.edit_name(old_name, new_name)
    if old_name == new_name:
        return Fore.YELLOW + "Name is already the same."
    return Fore.GREEN + "Contact name updated."


@input_error
def add_contact(args, book):
    if len(args) != 2:
        raise ValueError(Fore.RED + "Usage: add [name] [phone]")

    name, phone = args
    record = book.find(name)

    if record is None:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return Fore.GREEN + "Contact added."

    record.add_phone(phone)
    return Fore.GREEN + "Contact updated."


@input_error
def remove_contact(args, book):
    if len(args) != 1:
        raise ValueError(Fore.RED + "Usage: remove [name]")

    name = args[0]
    record = book.find(name)
    if record is None:
        raise ValueError(Fore.MAGENTA + f"Contact '{name}' not found.")

    book.delete(name)
    return Fore.GREEN + "Contact removed."


@input_error
def change_contact(args, book):
    if len(args) != 3:
        raise ValueError(Fore.RED + "Usage: change [name] [old phone] [new phone]")

    name, old_phone, new_phone = args
    record = book.find(name)
    if record is None:
        raise ValueError(Fore.MAGENTA + f"Contact '{name}' not found.")

    record.edit_phone(old_phone, new_phone)
    return Fore.GREEN + "Contact updated."


@input_error
def show_phone(args, book):
    if len(args) != 1:
        raise ValueError(Fore.RED + "Usage: phone [name]")

    name = args[0]
    record = book.find(name)
    if record is None:
        raise ValueError(Fore.MAGENTA + f"Contact '{name}' not found.")

    return (
        Fore.GREEN + "; ".join(str(phone) for phone in record.phones)
        or Fore.YELLOW + "No phone numbers saved."
    )


@input_error
def show_all(args, book):
    if args:
        raise ValueError(Fore.RED + "Usage: all")
    if not book.data:
        return Fore.GREEN + "Address book is empty."
    return "\n".join(str(record) for record in book.data.values())


@input_error
def add_birthday(args, book):
    if len(args) != 2:
        raise ValueError(Fore.RED + "Usage: add-birthday [name] [DD.MM.YYYY]")

    name, birthday = args
    record = book.find(name)
    if record is None:
        raise ValueError(Fore.MAGENTA + f"Contact '{name}' not found.")

    record.add_birthday(birthday)
    return Fore.GREEN + "Birthday added."


@input_error
def remove_birthday(args, book):
    if len(args) != 1:
        raise ValueError(Fore.RED + "Usage: remove-birthday [name]")

    name = args[0]
    record = book.find(name)
    if record is None:
        raise ValueError(Fore.MAGENTA + f"Contact '{name}' not found.")

    record.remove_birthday()
    return Fore.GREEN + "Birthday removed."


@input_error
def change_birthday(args, book):
    if len(args) != 2:
        raise ValueError(Fore.RED + "Usage: change-birthday [name] [DD.MM.YYYY]")

    name, new_birthday = args
    record = book.find(name)
    if record is None:
        raise ValueError(Fore.MAGENTA + f"Contact '{name}' not found.")

    record.edit_birthday(new_birthday)
    return Fore.GREEN + "Birthday updated."


@input_error
def show_birthday(args, book):
    if len(args) != 1:
        raise ValueError(Fore.RED + "Usage: show-birthday [name]")

    name = args[0]
    record = book.find(name)
    if record is None:
        raise ValueError(Fore.MAGENTA + f"Contact '{name}' not found.")
    if record.birthday is None:
        return Fore.YELLOW + "Birthday not set."

    return record.birthday.value.strftime("%d.%m.%Y")


@input_error
def birthdays(args, book):
    if args:
        raise ValueError(Fore.RED + "Usage: birthdays")

    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return Fore.GREEN + "No birthdays in the next 7 days."

    return "\n".join(
        f"{person['name']}: {person['congratulation_date']}" for person in upcoming
    )


@input_error
def add_email(args, book):
    if len(args) != 2:
        raise ValueError(Fore.RED + "Usage: add-email [name] [email@gmail.com]")

    name, email = args
    record = book.find(name)
    if record is None:
        raise ValueError(Fore.MAGENTA + f"Contact '{name}' not found.")
    record.add_email(email)
    return Fore.GREEN + "Email added"


@input_error
def change_email(args, book):
    if len(args) != 2:
        raise ValueError(Fore.RED + "Usage: [name] [new_email('email@gmail.com')]")

    name, new_email = args
    record = book.find(name)
    if record is None:
        raise ValueError(Fore.MAGENTA + f"Contact '{name}' not found.")
    record.edit_email(new_email)
    return Fore.GREEN + "Email changed"


@input_error
def remove_email(args, book):
    if len(args) != 1:
        raise ValueError(Fore.RED + "Usage: remove-email [name]")

    name = args[0]
    record = book.find(name)
    if record is None:
        raise ValueError(Fore.MAGENTA + f"Contact '{name}' not found.")
    record.remove_email()
    return Fore.GREEN + "Email removed"


@input_error
def add_address(args, book):
    if len(args) < 2:
        raise ValueError(Fore.RED + "Usage: add-address [name] [address]")

    name = args[0]
    address = " ".join(args[1:])
    record = book.find(name)
    if record is None:
        raise ValueError(Fore.MAGENTA + f"Contact '{name}' not found.")

    record.add_address(address)
    return Fore.GREEN + "Address added."


@input_error
def remove_address(args, book):
    if len(args) != 1:
        raise ValueError(Fore.RED + "Usage: remove-address [name]")
    name = args[0]
    record = book.find(name)
    if record is None:
        raise ValueError(Fore.MAGENTA + f"Contact '{name}' not found.")
    record.remove_address()
    return Fore.GREEN + "Address removed"


@input_error
def change_address(args, book):
    if len(args) < 2:
        raise ValueError(Fore.RED + "Usage: change-address [name] [new address]")

    name, new_address = args
    record = book.find(name)
    if record is None:
        raise ValueError(Fore.MAGENTA + f"Contact '{name}' not found.")
    record.edit_address(new_address)
    return Fore.GREEN + "Address updated"
