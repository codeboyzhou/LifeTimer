from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.validation import Number
from textual.widgets import Label, Input


class AgeInput(Horizontal):

    def __init__(self):
        super().__init__(id="age_input")

    def compose(self) -> ComposeResult:
        yield Label("I want to live to be")
        yield Input(
            id="input",
            placeholder="Please input a positive number here",
            type="integer",
            validators=[
                Number(minimum=50, maximum=200, failure_description="Available age should be between 50 and 200")
            ],
            validate_on=["blur"]
        )
        yield Label("years old")

    def on_input_blurred(self, event: Input.Blurred) -> None:
        if event.input.id == "input" and len(event.validation_result.failure_descriptions) > 0:
            error_message = event.validation_result.failure_descriptions[0]
            self.notify(title="Error Input", message=error_message, severity="error")

    @property
    def value(self) -> int | None:
        value = self.query_one("#input", Input).value
        return int(value) if value else None
