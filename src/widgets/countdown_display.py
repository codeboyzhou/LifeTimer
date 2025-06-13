from textual.reactive import reactive
from textual.widgets import Digits


class CountdownDisplay(Digits):
    """A widget to display ETA time."""

    time = reactive(0)

    def __init__(self):
        super().__init__(id="countdown_display")
        self.update_timer = None

    def on_mount(self):
        interval_seconds: float = 1 / 60
        self.update_timer = self.set_interval(interval_seconds, self.update_time)
        self.update_timer.pause()

    def set_time(self, time: int):
        self.time = time

    def update_time(self):
        self.time -= 1

    def watch_time(self, time: int):
        self.update(str(time))

    def start(self):
        self.update_timer.resume()
