from datetime import datetime

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button

from widgets.age_input import AgeInput
from widgets.birthday_picker import BirthdayPicker
from widgets.countdown_display import CountdownDisplay


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
        yield BirthdayPicker()
        yield AgeInput()
        yield Button(label="OK, Let's GO!", variant="primary", id="ok-button")
        yield CountdownDisplay()
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Called when the user presses the OK button."""
        if event.button.id == "ok-button":
            birthday_picker = self.query_one("#birthday_picker", BirthdayPicker)
            if birthday_picker.value is None:
                self.notify(message="Please select your birthday!", title="Error", severity="error")
                return

            age_input = self.query_one("#age_input", AgeInput)
            if age_input.value is None:
                self.notify(message="Please enter the age you want to live to!", title="Error", severity="error")
                return

            birthday_picker_values = birthday_picker.value.split("-")
            life_end_year = int(birthday_picker_values[0]) + age_input.value
            life_end_date = f"{life_end_year}-{birthday_picker_values[1]}-{birthday_picker_values[2]}"
            life_end_time = datetime.strptime(life_end_date, "%Y-%m-%d").timestamp()
            life_countdown_ms = (life_end_time - datetime.now().timestamp()) * 1000
            countdown_display = self.query_one("#countdown_display", CountdownDisplay)
            countdown_display.set_time(int(life_countdown_ms))
            countdown_display.start()

    def action_quit(self) -> None:
        """Called when the user presses the q key (or closes the app)."""
        self.exit()


if __name__ == "__main__":
    LifeTimerApp().run()
