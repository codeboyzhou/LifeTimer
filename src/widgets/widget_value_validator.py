from functools import wraps
from typing import Callable, Tuple, Type

from textual.widget import Widget


def validator(*input_fields: Tuple[str, Type[Widget], str]):
    """
    Decorator for validating input fields.

    This decorator can be used to validate input fields in a widget.
    It takes a list of tuples as arguments, where each tuple represents an input field.

    The first element of the tuple is the ID of the widget.
    The second element is the type of the widget.
    The third element is the error message to be displayed if the widget value is None.
    """

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(self: Widget, *args, **kwargs):
            for widget_id, widget_type, error_message in input_fields:
                widget = self.query_one(f"#{widget_id}", widget_type)
                if widget.value is None:
                    self.notify(message=error_message, title="Error", severity="error")
                    return None
            return func(self, *args, **kwargs)

        return wrapper

    return decorator
