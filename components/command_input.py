"""Command input with autocomplete, syntax suggestions and history."""

from textual.containers import Vertical
from textual.widgets import Input, Static
from textual.suggester import SuggestFromList

from commands import COMMANDS


class CommandInput(Vertical):
    def compose(self):
        yield Static("", id="command-suggestions", markup=False)

        yield HistoryInput(
            placeholder="Enter a command...",
            id="command",
            suggester=SuggestFromList(
                list(COMMANDS.keys()),
                case_sensitive=False,
            ),
        )

    def on_input_changed(self, event: Input.Changed):
        words = event.value.lower().split()
        suggestions = self.query_one("#command-suggestions", Static)

        # Find command syntax matching the entered command.
        matches = [
            syntax for command, syntax in COMMANDS.items()
            if words and command.startswith(words[0])
        ]

        suggestions.update("\n".join(matches))
        suggestions.display = bool(matches)


class HistoryInput(Input):
    """Input field supporting navigation through previous commands."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.history = []
        self.index = 0

    def on_input_submitted(self, event: Input.Submitted):
        # Store non-empty commands in history.
        if event.value.strip():
            self.history.append(event.value)

        self.index = len(self.history)

    def on_key(self, event):
        # Navigate command history using the arrow keys.
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

        # Move the cursor to the end of the restored command.
        self.cursor_position = len(self.value)
        event.prevent_default()
        event.stop()