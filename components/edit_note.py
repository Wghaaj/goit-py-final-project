"""Dialog for editing existing notes."""

from textual.screen import ModalScreen
from textual.containers import Vertical, Horizontal
from textual.widgets import Label, Input, Button


class EditNote(ModalScreen):
    def __init__(self, text):
        super().__init__()
        self.text = text

    def compose(self):
        with Vertical(id="edit-dialog"):
            yield Label("Edit note")
            yield Input(value=self.text, id="edit-text")

            with Horizontal():
                yield Button("Cancel", id="cancel")
                yield Button("Save", id="save")

    def on_button_pressed(self, event: Button.Pressed):
        text = self.query_one("#edit-text", Input).value

        # Return the edited text or None if editing is cancelled.
        self.dismiss(text if event.button.id == "save" else None)