"""Route commands to their corresponding backend handlers."""

from rich.text import Text

import contact_commands as cc
from note_commands import NOTE_COMMANDS


COMMAND_HANDLERS = {
    # Contacts
    "add": cc.add_contact,
    "remove": cc.remove_contact,
    "change-name": cc.change_name,
    "change": cc.change_contact,
    "phone": cc.show_phone,
    "all": cc.show_all,
    "search": cc.search_contacts,

    # Email
    "add-email": cc.add_email,
    "change-email": cc.change_email,
    "remove-email": cc.remove_email,

    # Address
    "add-address": cc.add_address,
    "change-address": cc.change_address,
    "remove-address": cc.remove_address,

    # Birthdays
    "add-birthday": cc.add_birthday,
    "change-birthday": cc.change_birthday,
    "remove-birthday": cc.remove_birthday,
    "show-birthday": cc.show_birthday,
    "birthdays": cc.birthdays,
}


def execute_command(command, args, book, notebook):
    # Note commands require access to both contacts and notes.
    if command in NOTE_COMMANDS:
        return NOTE_COMMANDS[command](args, book, notebook)

    handler = COMMAND_HANDLERS.get(command)

    if handler is None:
        return "Error: Invalid command."

    result = handler(args, book)

    # Strip colour formatting before checking for errors.
    if Text.from_ansi(result).plain.startswith("Error:"):
        return result

    # Keep linked notes consistent when contacts are deleted or renamed.
    if command == "remove":
        notebook.on_contact_deleted(args[0])

    elif command == "change-name":
        notebook.on_contact_renamed(*args)

    return result