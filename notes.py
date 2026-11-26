"""Notes with tags and an optional link to a contact.

Note     - one text note: id, text, tags, optional contact name.
Notebook - all notes, keyed by id (UserDict).

A note does not belong to a contact: it can exist without one.
The contact is stored only by name (association, not composition),
so deleting a contact never deletes its notes.
"""
import re
from collections import UserDict
from datetime import datetime

MAX_TEXT_LENGTH = 500
TAG_PATTERN = re.compile(r"[\w-]{1,30}")


class NoteError(ValueError):
    """Invalid note data or a note that does not exist."""


def validate_text(text: str) -> str:
    """Return stripped text or raise NoteError if it is empty or too long."""
    text = text.strip()
    if not text:
        raise NoteError("Note text cannot be empty.")
    if len(text) > MAX_TEXT_LENGTH:
        raise NoteError(
            f"Note is too long: {len(text)} characters "
            f"(max {MAX_TEXT_LENGTH})."
        )
    return text


def normalize_tag(tag: str) -> str:
    """Return a tag in lower case without '#'. Raise NoteError if invalid.

    Allowed: letters (any language), digits, '_' and '-', up to 30 chars.
    """
    tag = tag.strip().lstrip("#").lower()
    if not TAG_PATTERN.fullmatch(tag):
        raise NoteError(
            f"Invalid tag: '{tag}'. Use letters, digits, '_' or '-' "
            "(up to 30 characters)."
        )
    return tag


class Note:
    """A text note with tags and an optional linked contact."""

    def __init__(self, note_id: int, text: str):
        self.id = note_id
        self.text = validate_text(text)
        self.tags: set[str] = set()
        self.contact: str | None = None
        self.created = datetime.now()
        self.updated = self.created

    def edit(self, new_text: str) -> None:
        self.text = validate_text(new_text)
        self.updated = datetime.now()

    def add_tag(self, tag: str) -> None:
        self.tags.add(normalize_tag(tag))

    def remove_tag(self, tag: str) -> None:
        tag = normalize_tag(tag)
        if tag not in self.tags:
            raise NoteError(f"Note #{self.id} has no tag '{tag}'.")
        self.tags.remove(tag)

    def matches(self, query: str) -> bool:
        """Case-insensitive search in text, tags and contact name."""
        query = query.lower()
        return (
            query in self.text.lower()
            or any(query in tag for tag in self.tags)
            or (self.contact is not None and query in self.contact.lower())
        )

    def __str__(self) -> str:
        line = f"#{self.id} {self.text}"
        if self.tags:
            line += "  " + " ".join(f"#{tag}" for tag in sorted(self.tags))
        if self.contact:
            line += f"  (contact: {self.contact})"
        return line


class Notebook(UserDict):
    """All notes. Key is the note id, value is the Note."""

    def __init__(self):
        super().__init__()
        self.next_id = 1

    # --- basic operations -------------------------------------------------

    def add_note(self, text: str) -> Note:
        note = Note(self.next_id, text)
        self.data[note.id] = note
        self.next_id += 1
        return note

    def get_note(self, note_id: int) -> Note:
        note = self.data.get(note_id)
        if note is None:
            raise NoteError(f"Note #{note_id} not found.")
        return note

    def edit_note(self, note_id: int, new_text: str) -> Note:
        note = self.get_note(note_id)
        note.edit(new_text)
        return note

    def delete_note(self, note_id: int) -> None:
        self.get_note(note_id)
        del self.data[note_id]
        self.next_id = max(self.data, default=0) + 1

    # --- search and tags --------------------------------------------------

    def search(self, query: str) -> list[Note]:
        query = query.strip()
        if not query:
            raise NoteError("Search query cannot be empty.")
        return [note for note in self.data.values() if note.matches(query)]

    def find_by_tag(self, tag: str) -> list[Note]:
        tag = normalize_tag(tag)
        return [note for note in self.data.values() if tag in note.tags]

    def sorted_by_tags(self) -> list[Note]:
        """Notes sorted by their tags alphabetically; untagged notes last."""
        return sorted(
            self.data.values(),
            key=lambda note: (not note.tags, sorted(note.tags), note.id),
        )

    def group_by_tags(self) -> dict[str, list[Note]]:
        """{tag: notes} with tags in alphabetical order.

        A note with several tags appears in several groups.
        Untagged notes are collected under the key "".
        """
        groups: dict[str, list[Note]] = {}
        for note in self.data.values():
            for tag in note.tags or {""}:
                groups.setdefault(tag, []).append(note)
        return {
            tag: groups[tag]
            for tag in sorted(groups, key=lambda tag: (tag == "", tag))
        }

    # --- link to contacts -------------------------------------------------

    def link_contact(self, note_id: int, contact_name: str) -> Note:
        note = self.get_note(note_id)
        note.contact = contact_name
        return note

    def unlink_contact(self, note_id: int) -> Note:
        note = self.get_note(note_id)
        if note.contact is None:
            raise NoteError(f"Note #{note_id} is not linked to a contact.")
        note.contact = None
        return note

    def notes_for_contact(self, contact_name: str) -> list[Note]:
        return [
            note for note in self.data.values()
            if note.contact == contact_name
        ]

    def on_contact_renamed(self, old_name: str, new_name: str) -> None:
        """Call after a contact is renamed: keep its notes linked."""
        for note in self.notes_for_contact(old_name):
            note.contact = new_name

    def on_contact_deleted(self, contact_name: str) -> None:
        """Call after a contact is deleted: its notes stay, without a link."""
        for note in self.notes_for_contact(contact_name):
            note.contact = None