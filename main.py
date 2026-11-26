from colorama import Fore, Style, init
from contact_commands import (
    change_name,
    add_contact,
    change_contact,
    remove_contact,
    show_phone,
    show_all,
    add_birthday,
    show_birthday,
    birthdays,
    remove_birthday,
    change_birthday,
    add_email,
    remove_email,
    change_email,
    add_address,
    remove_address,
    change_address,
)
from note_commands import NOTE_COMMANDS
from storage import load_data, save_data
from utils import parse_input


init(autoreset=True)


def main():
    book, notebook = load_data()
    print("Welcome to the assistant bot!")

    while True:
        try:
            user_input = input(
                Fore.CYAN + Style.BRIGHT + "Enter a command: " + Style.RESET_ALL
            )
        except (EOFError, KeyboardInterrupt):
            print("\nGood bye!")
            break

        command, args = parse_input(user_input)

        if command == "exit":
            print("Good bye!")
            break
        elif command in NOTE_COMMANDS:
            print(NOTE_COMMANDS[command](args, book, notebook))
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "remove":
            print(remove_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(args, book))
        elif command == "change-name":
            print(change_name(args, book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "remove-birthday":
            print(remove_birthday(args, book))
        elif command == "change-birthday":
            print(change_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        elif command == "add-email":
            print(add_email(args, book))
        elif command == "remove-email":
            print(remove_email(args, book))
        elif command == "change-email":
            print(change_email(args, book))
        elif command == "add-address":
            print(add_address(args, book))
        elif command == "remove-address":
            print(remove_address(args, book))
        elif command == "change-address":
            print(change_address(args, book))
        elif command:
            print("Invalid command.")

    save_data(book, notebook)


if __name__ == "__main__":
    main()
