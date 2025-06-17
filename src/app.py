from datetime import datetime
from typing import override

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button

from i18n import i18n
from widgets.age_input import AgeInput
from widgets.birthday_picker import BirthdayPicker
from widgets.countdown_display import CountdownDisplay
from widgets.widget_value_validators import widget_value_validators, WidgetValueValidator, NumberInputValidator

_ = i18n()


class LifeTimerApp(App):
    """
    An interesting terminal application that visualizes your life's remaining time.
    """

    TITLE = "Life Timer"
    """Main title for the application."""

    CSS_PATH = "app.tcss"
    """Define the path to the CSS stylesheet used by the application."""

    BINDINGS = [
        ("q", "quit", _("Quit")),
        ("d", "toggle_dark_mode", _("Toggle Dark/Light Mode"))
    ]
    """Key bindings for the application."""

    @override
    def compose(self) -> ComposeResult:
        """Called to add widgets to the app."""
        yield Header(show_clock=True)
        yield BirthdayPicker()
        yield AgeInput()
        yield Button(label=_("OK, Let's GO!"), variant="primary", id="ok_button")
        yield CountdownDisplay()
        yield Footer()

    def _on_button_pressed(self, event: Button.Pressed) -> None:
        """Called when the user presses buttons."""
        if event.button.id == "ok_button":
            self._on_ok_button_pressed()

    @widget_value_validators(
        WidgetValueValidator(
            widget_id="birthday_picker", widget_type=BirthdayPicker,
            failure_message_i18n_id="Please select your birthday"
        ),
        NumberInputValidator(
            widget_id="age_input", widget_type=AgeInput, min=60, max=120,
            failure_message_i18n_id="Available age should be between 60 and 120"
        )
    )
    def _on_ok_button_pressed(self) -> None:
        """Called when the user presses the OK button."""
        birthday_picker = self.query_one("#birthday_picker", BirthdayPicker)
        age_input = self.query_one("#age_input", AgeInput)
        birthday_picker_values = birthday_picker.value.split("-")
        life_end_year = int(birthday_picker_values[0]) + age_input.value
        life_end_date = f"{life_end_year}-{birthday_picker_values[1]}-{birthday_picker_values[2]}"
        life_end_timestamp = datetime.strptime(life_end_date, "%Y-%m-%d").timestamp()
        life_countdown_seconds = life_end_timestamp - datetime.now().timestamp()
        countdown_display = self.query_one("#countdown_display", CountdownDisplay)
        countdown_display.set_start_seconds(int(life_countdown_seconds))
        countdown_display.start()

    def action_quit(self) -> None:
        """Called when the user presses the q key (or closes the app)."""
        self.exit()

    def action_toggle_dark_mode(self) -> None:
        self.theme = "textual-dark" if self.theme == "textual-light" else "textual-light"
