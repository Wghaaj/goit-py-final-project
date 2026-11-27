"""Contact book view and search functionality."""

from textual.containers import Vertical, Horizontal
from textual.widgets import Label, Input, Button, DataTable


class Contacts(Vertical):
    def compose(self):
        yield Label("Contact Book", classes="page-title")
        yield Label("Manage and view your saved contacts.")

        with Horizontal(id="contact-search"):
            yield Input(placeholder="Search contacts...", id="search-input")
            yield Button("Search", id="search-btn")

        yield DataTable(id="contact-table")
        yield Label("0 contacts found", id="contact-total")

    def on_mount(self):
        table = self.query_one("#contact-table", DataTable)
        table.zebra_stripes = True
        table.cursor_type = "row"

        table.add_column("Name", width=20)
        table.add_column("Phone", width=18)
        table.add_column("Email", width=28)
        table.add_column("Address", width=25)
        table.add_column("Birthday", width=15)

        self.refresh_contacts()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "search-btn":
            self.refresh_contacts()

    def on_input_submitted(self, event: Input.Submitted):
        if event.input.id == "search-input":
            self.refresh_contacts()
            event.stop()

    def refresh_contacts(self, records=None):
        table = self.query_one("#contact-table", DataTable)
        table.clear()

        # Display matching contacts or all contacts if the search is empty.
        if records is None:
            query = self.query_one("#search-input", Input).value.strip()
            book = self.app.book
            records = book.search(query) if query else list(book.values())

        for record in records:
            phones = ", ".join(str(phone) for phone in record.phones)
            birthday = (
                record.birthday.value.strftime("%d.%m.%Y")
                if record.birthday else "—"
            )
            email = record.email.value if record.email else "—"
            address = record.address.value if record.address else "—"

            table.add_row(
                record.name.value, phones, email, address, birthday
            )

        # Update the number of displayed contacts.
        self.query_one("#contact-total", Label).update(
            f"{len(records)} contacts found"
        )