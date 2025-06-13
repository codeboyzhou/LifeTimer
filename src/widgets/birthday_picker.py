from datetime import datetime

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Select, Label


class BirthdayPicker(Horizontal):
    """A widget for selecting a date."""

    def __init__(self, min_year: int = 1970, max_year: int | None = None):
        """
        Initialize the date picker with specified minimum and maximum years.

        Args:
            min_year (int): The minimum year available in the date picker. Defaults to 1970.
            max_year (int | None): The maximum year available in the date picker. If None, defaults to the current year.

        Attributes:
            months (List[Tuple[str, int]]): A list of tuples
            where each tuple contains the name of a month and its numerical representation (1-12).
        """

        super().__init__(id="birthday_picker")
        self.min_year = min_year
        self.max_year = max_year if max_year else datetime.now().year
        self.months = [
            ("01", 1), ("02", 2), ("03", 3), ("04", 4),
            ("05", 5), ("06", 6), ("07", 7), ("08", 8),
            ("09", 9), ("10", 10), ("11", 11), ("12", 12)
        ]

    def compose(self) -> ComposeResult:
        """
        Called by Textual to create child widgets. Inherited from the super class and override here.
        """

        years = [(str(year), year) for year in range(self.min_year, self.max_year + 1)]
        years.reverse()  # Display in descending order starting from the current year

        yield Label("Please select your birthday")
        yield Select(years, id="year-select", prompt="Please select the year")
        yield Select(self.months, id="month-select", prompt="Please select the month")
        yield Select([], id="day-select", prompt="Please select the day")

    def on_select_changed(self, event: Select.Changed) -> None:
        """
        Called when any select widget's value changes.

        Args:
            event (Select.Changed): The event object containing information about the changed select widget.
        """

        if event.select.id in ["year-select", "month-select"]:
            year_select = self.query_one("#year-select", Select)
            month_select = self.query_one("#month-select", Select)
            if year_select.value and month_select.value:
                self._update_days(year_select.value, month_select.value)

    def _update_days(self, year: int, month: int) -> None:
        """
        Update the available days in the day select widget based on the selected year and month.

        Args:
            year (int): The selected year.
            month (int): The selected month.
        """

        if month == 2:
            if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
                days = 29
            else:
                days = 28
        elif month in [4, 6, 9, 11]:
            days = 30
        else:
            days = 31

        day_select = self.query_one("#day-select", Select)
        day_options = [(str(day).zfill(2), day) for day in range(1, days + 1)]
        day_select.set_options(day_options)

    @property
    def value(self) -> str | None:
        year_select = self.query_one("#year-select", Select)
        month_select = self.query_one("#month-select", Select)
        day_select = self.query_one("#day-select", Select)
        if year_select.value == Select.BLANK or month_select.value == Select.BLANK or day_select.value == Select.BLANK:
            return None
        return f"{year_select.value}-{str(month_select.value).zfill(2)}-{str(day_select.value).zfill(2)}"
