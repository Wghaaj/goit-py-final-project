from textual.containers import Vertical
from textual.widgets import Input, Static
from textual.suggester import SuggestFromList
from commands import COMMANDS


class CommandInput(Vertical):

    def compose(self):
        yield Static("", id="command-suggestions")

        yield HistoryInput(
            placeholder="Enter a command...",
            id="command",
            suggester=SuggestFromList(
                list(COMMANDS.keys()),
                case_sensitive=False
            )
        )

    def on_input_changed(self, event: Input.Changed):
        value = event.value.lower().split()
        suggestions = self.query_one("#command-suggestions", Static)

        matches = [
            syntax for command, syntax in COMMANDS.items()
            if value and command.startswith(value[0])
        ]

        suggestions.update("\n".join(matches))
        suggestions.display = bool(matches)

class HistoryInput(Input):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.history = []
        self.index = 0

    def on_input_submitted(self, event: Input.Submitted):
        if event.value.strip():
            self.history.append(event.value)
        self.index = len(self.history)

    def on_key(self, event):
        if event.key == "up" and self.index > 0:
            self.index -= 1
        elif event.key == "down" and self.index < len(self.history):
            self.index += 1
        else:
            return

        self.value = (
            self.history[self.index]
            if self.index < len(self.history) else ""
        )

        self.cursor_position = len(self.value)
        event.prevent_default()
        event.stop()