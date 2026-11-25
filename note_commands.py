"""Command handlers for notes.

Every handler has the same signature: handler(args, book, notebook) -> str.
`book` is needed only for linking notes to contacts.
All handlers are collected in NOTE_COMMANDS at the end of the file.
"""
from functools import wraps

from colorama import Fore

from notes import Note, NoteError, Notebook


def note_error(func):
    """Turn note errors into a red message so the bot never crashes."""
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NoteError as error:
            return Fore.RED + f"Error: {error}"
        except (ValueError, IndexError, KeyError):
            return Fore.RED + "Error: Invalid command arguments."
    return inner


def parse_id(value: str) -> int:
    """'3' or '#3' -> 3. Raise NoteError for anything else."""
    value = value.lstrip("#")
    if not value.isdigit():
        raise NoteError(f"Note id must be a number, got: '{value}'.")
    return int(value)


def format_notes(notes: list[Note], empty_message: str) -> str:
    if not notes:
        return Fore.YELLOW + empty_message
    return "\n".join(str(note) for note in notes)


@note_error
def add_note(args, book, notebook: Notebook) -> str:
    if not args:
        raise NoteError("Usage: add-note [text]")
    note = notebook.add_note(" ".join(args))
    return Fore.GREEN + f"Note #{note.id} added."


@note_error
def show_notes(args, book, notebook: Notebook) -> str:
    if args:
        raise NoteError("Usage: notes")
    return format_notes(list(notebook.data.values()), "No notes yet.")


@note_error
def show_note(args, book, notebook: Notebook) -> str:
    if len(args) != 1:
        raise NoteError("Usage: show-note [id]")
    note = notebook.get_note(parse_id(args[0]))
    created = note.created.strftime("%d.%m.%Y %H:%M")
    updated = note.updated.strftime("%d.%m.%Y %H:%M")
    return f"{note}\ncreated: {created}, updated: {updated}"


@note_error
def find_note(args, book, notebook: Notebook) -> str:
    if not args:
        raise NoteError("Usage: find-note [text]")
    query = " ".join(args)
    return format_notes(notebook.search(query), f"Nothing found for '{query}'.")


@note_error
def edit_note(args, book, notebook: Notebook) -> str:
    if len(args) < 2:
        raise NoteError("Usage: edit-note [id] [new text]")
    note = notebook.edit_note(parse_id(args[0]), " ".join(args[1:]))
    return Fore.GREEN + f"Note #{note.id} updated."


@note_error
def delete_note(args, book, notebook: Notebook) -> str:
    if len(args) != 1:
        raise NoteError("Usage: delete-note [id]")
    note_id = parse_id(args[0])
    notebook.delete_note(note_id)
    return Fore.GREEN + f"Note #{note_id} deleted."


@note_error
def add_tag(args, book, notebook: Notebook) -> str:
    if len(args) < 2:
        raise NoteError("Usage: add-tag [id] [tag] [tag ...]")
    note = notebook.get_note(parse_id(args[0]))
    for tag in args[1:]:
        note.add_tag(tag)
    return Fore.GREEN + f"Tags of note #{note.id}: " + ", ".join(sorted(note.tags))


@note_error
def remove_tag(args, book, notebook: Notebook) -> str:
    if len(args) != 2:
        raise NoteError("Usage: remove-tag [id] [tag]")
    note = notebook.get_note(parse_id(args[0]))
    note.remove_tag(args[1])
    return Fore.GREEN + f"Tag removed from note #{note.id}."


@note_error
def find_tag(args, book, notebook: Notebook) -> str:
    if len(args) != 1:
        raise NoteError("Usage: find-tag [tag]")
    return format_notes(
        notebook.find_by_tag(args[0]), f"No notes with tag '{args[0]}'."
    )


@note_error
def sort_notes(args, book, notebook: Notebook) -> str:
    """Notes grouped by tags in alphabetical order."""
    if args:
        raise NoteError("Usage: sort-notes")
    groups = notebook.group_by_tags()
    if not groups:
        return Fore.YELLOW + "No notes yet."
    lines = []
    for tag, notes in groups.items():
        title = f"#{tag}" if tag else "(no tags)"
        lines.append(Fore.CYAN + title)
        lines.extend(f"  {note}" for note in notes)
    return "\n".join(lines)


@note_error
def link_note(args, book, notebook: Notebook) -> str:
    if len(args) != 2:
        raise NoteError("Usage: link-note [id] [contact name]")
    note_id, name = parse_id(args[0]), args[1]
    if book.find(name) is None:
        raise NoteError(f"Contact '{name}' not found.")
    notebook.link_contact(note_id, name)
    return Fore.GREEN + f"Note #{note_id} linked to {name}."


@note_error
def unlink_note(args, book, notebook: Notebook) -> str:
    if len(args) != 1:
        raise NoteError("Usage: unlink-note [id]")
    note = notebook.unlink_contact(parse_id(args[0]))
    return Fore.GREEN + f"Note #{note.id} unlinked."


@note_error
def contact_notes(args, book, notebook: Notebook) -> str:
    if len(args) != 1:
        raise NoteError("Usage: contact-notes [contact name]")
    name = args[0]
    if book.find(name) is None:
        raise NoteError(f"Contact '{name}' not found.")
    return format_notes(
        notebook.notes_for_contact(name), f"{name} has no notes."
    )


NOTE_COMMANDS = {
    "add-note": add_note,
    "notes": show_notes,
    "show-note": show_note,
    "find-note": find_note,
    "edit-note": edit_note,
    "delete-note": delete_note,
    "add-tag": add_tag,
    "remove-tag": remove_tag,
    "find-tag": find_tag,
    "sort-notes": sort_notes,
    "link-note": link_note,
    "unlink-note": unlink_note,
    "contact-notes": contact_notes,
}