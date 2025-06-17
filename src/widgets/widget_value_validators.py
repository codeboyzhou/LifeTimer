from functools import wraps
from typing import Callable, Type, TypeVar

from pydantic import BaseModel
from textual.app import App
from textual.widget import Widget

from i18n import i18n

_ = i18n()

WidgetType = TypeVar("WidgetType", bound=Widget)


class WidgetValueValidator(BaseModel):
    widget_id: str
    widget_type: Type[WidgetType]
    failure_message_i18n_id: str


class NumberInputValidator(WidgetValueValidator):
    min: int | float
    max: int | float


def widget_value_validators(*validators: WidgetValueValidator):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(self: App, *args, **kwargs):
            failure_message = None
            for validator in validators:
                widget = self.query_one(f"#{validator.widget_id}", validator.widget_type)

                if widget.value is None:
                    failure_message = _(validator.failure_message_i18n_id)
                    break

                if isinstance(validator, NumberInputValidator):
                    if widget.value < validator.min or widget.value > validator.max:
                        failure_message = _(validator.failure_message_i18n_id)
                        break

            if failure_message is not None:
                self.notify(message=failure_message, title=_("Error"), severity="error")
                return None

            return func(self, *args, **kwargs)

        return wrapper

    return decorator
