from textual.app import App, ComposeResult
from textual.widgets import Header, Footer

from widgets.date_picker import DatePicker
from widgets.age_input import AgeInput


class LifeTimerApp(App):
    """An interesting terminal application that visualizes your life's remaining time."""

    TITLE = "Life Timer"
    """Main title for the application."""

    CSS_PATH = "life_timer_app.tcss"
    """Define the path to the CSS stylesheet used by the application."""

    BINDINGS = [
        ("q", "quit", "Quit")
    ]
    """Key bindings for the application."""

    def compose(self) -> ComposeResult:
        """Called to add widgets to the app."""
        yield Header(show_clock=True)
        yield DatePicker()
        yield AgeInput()
        yield Footer()

    def action_quit(self) -> None:
        """Called when the user presses the q key (or closes the app)."""
        self.exit()


if __name__ == "__main__":
    LifeTimerApp().run()
