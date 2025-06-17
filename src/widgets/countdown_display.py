from textual.reactive import reactive
from textual.widgets import Digits


class CountdownDisplay(Digits):
    """A widget to display ETA time."""

    start_seconds = reactive(0)

    def __init__(self):
        super().__init__(id="countdown_display")
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
