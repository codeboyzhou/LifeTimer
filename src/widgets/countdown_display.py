from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.reactive import reactive
from textual.widgets import Digits, Label

from i18n import i18n

_ = i18n()


class TimeDisplay(Digits):
    """A widget to display ETA time."""

    start_seconds = reactive(0)

    def __init__(self):
        super().__init__(id="time_display")
        self.update_timer = None

    def on_mount(self):
        interval_seconds = 1
        self.update_timer = self.set_interval(interval_seconds, self.update_time)
        self.update_timer.pause()

    def set_start_seconds(self, seconds: int):
        self.start_seconds = seconds

    def update_time(self):
        self.start_seconds -= 1

    def watch_start_seconds(self, seconds: int):
        self.update(str(seconds))

    def start(self):
        self.update_timer.resume()


class CountdownDisplay(Horizontal):

    def __init__(self):
        super().__init__(id="countdown_display")

    def compose(self) -> ComposeResult:
        yield Label(_("You still have"))
        yield TimeDisplay()
        yield Label(_("seconds remaining in your expected lifespan."))

    def start(self, life_countdown_seconds: int):
        time_display = self.query_one("#time_display", TimeDisplay)
        time_display.set_start_seconds(life_countdown_seconds)
        time_display.start()
