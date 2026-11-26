import contact_commands as cc
from note_commands import NOTE_COMMANDS
from rich.text import Text



COMMAND_HANDLERS = {
    "add": cc.add_contact,
    "remove": cc.remove_contact,
    "change": cc.change_contact,
    "change-name": cc.change_name,
    "phone": cc.show_phone,
    "all": cc.show_all,

    "add-email": cc.add_email,
    "change-email": cc.change_email,
    "remove-email": cc.remove_email,

    "add-address": cc.add_address,
    "change-address": cc.change_address,
    "remove-address": cc.remove_address,

    "add-birthday": cc.add_birthday,
    "change-birthday": cc.change_birthday,
    "remove-birthday": cc.remove_birthday,
    "show-birthday": cc.show_birthday,
    "birthdays": cc.birthdays,

}

def execute_command(command, args, book, notebook):
    if command in NOTE_COMMANDS:
        return NOTE_COMMANDS[command](args, book, notebook)

    handler = COMMAND_HANDLERS.get(command)

    if handler is None:
        return "Error: Invalid command."

    result = handler(args, book)

    if Text.from_ansi(result).plain.startswith("Error:"):
        return result

    if command == "remove":
        notebook.on_contact_deleted(args[0])

    elif command == "change-name":
        notebook.on_contact_renamed(*args)

    return result