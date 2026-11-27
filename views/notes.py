from textual.containers import Vertical, Horizontal
from textual.widgets import Label, Input, Button, DataTable

from components.confirmation import Confirmation
from components.edit_note import EditNote


class Notes(Vertical):
    def compose(self):
        yield Label("Your Notes", classes="page-title")
        yield Label("Organize and manage notes linked to your contacts.")

        with Horizontal(id="note-search"):
            yield Input(placeholder="Search notes...", id="note-search-input")
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
                key=str(note.id),
            )

        self.query_one("#note-total", Label).update(
            f"{len(notes)} notes found"
        )

    def search_notes(self):
        query = self.query_one("#note-search-input", Input).value.strip()
        results = self.app.notebook.search(query) if query else None
        self.refresh_notes(results)

    def on_button_pressed(self, event: Button.Pressed):
        button = event.button.id

        if button == "note-search-btn":
            self.search_notes()
            return

        table = self.query_one("#note-table", DataTable)
        if not table.row_count:
            self.app.notify("No note selected.", severity="warning")
            return

        note_id = str(table.get_row_at(table.cursor_row)[0])

        if button == "view-note":
            self.app.process_command("show-note", [note_id])
        elif button == "edit-note":
            self.edit_selected_note(note_id)
        elif button == "delete-note":
            self.app.push_screen(
                Confirmation(f"Are you sure you want to delete note #{note_id}?"),
                lambda confirmed: self.app.process_command(
                    "delete-note", [note_id]
                ) if confirmed else None,
            )

    def edit_selected_note(self, note_id):
        note = self.app.notebook.get_note(int(note_id))
        self.app.push_screen(
            EditNote(note.text),
            lambda text: self.app.process_command(
                "edit-note", [note_id, text]
            ) if text is not None else None,
        )

    def on_input_submitted(self, event: Input.Submitted):
        if event.input.id == "note-search-input":
            self.search_notes()
            event.stop()
