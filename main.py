from colorama import Fore, Style, init
from contact_commands import (
    add_contact, change_contact, show_phone, show_all,
    add_birthday, show_birthday, birthdays,
)
from storage import load_data, save_data
from utils import parse_input


init(autoreset=True)


def main():
    book = load_data()
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

        if command in ("close", "exit"):
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(args, book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        elif command:
            print("Invalid command.")

    save_data(book)


if __name__ == "__main__":
    main()
