from textual.containers import Vertical
from textual.widgets import Input, Static
from textual.suggester import SuggestFromList
from commands import COMMANDS


class CommandInput(Vertical):

    def compose(self):
        yield Static("", id="command-suggestions")

        yield Input(
            placeholder="Enter a command...",
            id="command",
            suggester=SuggestFromList(
                list(COMMANDS.keys()),
                case_sensitive=False
            )
        )

    def on_input_changed(self, event: Input.Changed):
        value = event.value.lower()

        suggestions = self.query_one(
            "#command-suggestions", Static
        )

        if not value or " " in value:
            suggestions.display = False
            return

        matches = [
            f"{command:<20} {description}"
            for command, description in COMMANDS.items()
            if command.startswith(value)
        ]

        if matches:
            suggestions.update("\n".join(matches))
            suggestions.display = True
        else:
            suggestions.display = False