from textual.screen import ModalScreen
from textual.containers import Vertical, Horizontal
from textual.widgets import Label, Button


class Confirmation(ModalScreen):

    def compose(self):
        with Vertical(id="confirmation"):
            yield Label("Are you sure you want to delete this item?")

            with Horizontal():
                yield Button("Cancel", id="cancel")
                yield Button("Delete", id="delete", variant="error")

    def on_button_pressed(self, event: Button.Pressed):
        self.dismiss(event.button.id == "delete")