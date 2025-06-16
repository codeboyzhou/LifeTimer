from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Label, Input

from i18n import i18n

_ = i18n()


class AgeInput(Horizontal):

    def __init__(self):
        super().__init__(id="age_input")

    def compose(self) -> ComposeResult:
        yield Label(_("I want to live to be"))
        yield Input(id="input", type="integer", placeholder=_("Please input an integer between 60 and 120 here"))
        yield Label(_("years old"))

    @property
    def value(self) -> int | None:
        value = self.query_one("#input", Input).value
        return int(value) if value else None
