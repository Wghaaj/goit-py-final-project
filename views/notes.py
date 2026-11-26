from textual.containers import Vertical, Horizontal
from textual.widgets import Label, Input, Button, DataTable


class Notes(Vertical):

    def compose(self):
        yield Label("Your Notes", classes="page-title")
        yield Label(
            "Organize and manage notes linked to your contacts."
        )

        with Horizontal(id="note-search"):
            yield Input(
                placeholder="Search notes...",
                id="note-search-input"
            )
            yield Button("Search", id="note-search-btn")

        yield DataTable(id="note-table")
        yield Label("0 notes found", id="note-total")

        with Horizontal(id="note-actions"):
            yield Button("View note", id="view-note")
            yield Button("Edit note", id="edit-note")
            yield Button("Delete note", id="delete-note")

    def on_mount(self):
        table = self.query_one("#note-table", DataTable)
        table.zebra_stripes = True

        table.add_column("ID", width=6)
        table.add_column("Contact", width=20)
        table.add_column("Note", width=45)
        table.add_column("Tags", width=20)

        table.cursor_type = "row"

        self.refresh_notes()

    def refresh_notes(self, notes=None):
        table = self.query_one("#note-table", DataTable)
        table.clear()

        if notes is None:
            notes = list(self.app.notebook.values())

        for note in notes:
            table.add_row(
                str(note.id),
                note.contact or "—",
                note.text,
                ", ".join(sorted(note.tags)) or "—",
                key=str(note.id)
            )

        self.query_one("#note-total", Label).update(
            f"{len(notes)} notes found"
        )