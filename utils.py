"""Command parsing and input error handling."""

from functools import wraps

from colorama import Fore


def input_error(func):
    """Convert command errors into user-friendly messages."""
    @wraps(func)
    def inner(args, book):
        try:
            return func(args, book)
        except ValueError as error:
            return Fore.RED + f"Error: {error}"
        except (IndexError, KeyError):
            return Fore.RED + "Error: Invalid command arguments."

    return inner


def parse_input(user_input):
    """Separate the command name from its arguments."""
    parts = user_input.strip().split()

    if not parts:
        return "", []

    return parts[0].lower(), parts[1:]