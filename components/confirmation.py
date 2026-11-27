"""Reusable deletion confirmation dialog."""

from textual.screen import ModalScreen
from textual.containers import Vertical, Horizontal
from textual.widgets import Label, Button


class Confirmation(ModalScreen):
    def __init__(self, message):
        super().__init__()
        self.message = message

    def compose(self):
        with Vertical(id="confirmation"):
            yield Label(self.message, markup=False)

            with Horizontal():
                yield Button("Cancel", id="cancel")
                yield Button("Delete", id="delete", variant="error")

    def on_button_pressed(self, event: Button.Pressed):
        # Return True only when deletion is confirmed.
        self.dismiss(event.button.id == "delete")