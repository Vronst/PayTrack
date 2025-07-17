from datetime import datetime

from . import Validator


class DateValidator(Validator):
    """Check if passed value is correct date.
    Takse to params, future_date and past_date.

    Params:
        future_date (bool): if True, date must be later than datetime.now()
        (unless its the same day), defaults to False.

        past_date (bool): if True, date must be earlier than datetime.now()
        (unless its the same day), defaults to False.

        If both are True or both are False, no time constraint is applied.
    """

    def __init__(self, future_date: bool = False, past_date: bool = False):
        if future_date and past_date:
            pass
        else:
            self.future = future_date
            self.past = past_date

    def __call__(self, key, value: str | datetime) -> datetime:
        formats: list[str] = [
            "%d-%m-%y",
            "%d-%m-%Y",
            "%Y-%m-%d",
        ]
        if isinstance(value, str):
            for format in formats:
                try:
                    value = datetime.strptime(value, format)
                except ValueError:
                    continue
                else:
                    break

        if not isinstance(value, datetime):
            raise ValueError(
                f"{key} -\
            Invalid datetime string format: {value}"
            )

        now = datetime.now(tz=value.tzinfo) if value.tzinfo else datetime.now()
        absolute = abs(value - now).days

        if self.future and value < now and absolute != 0:
            raise ValueError(f"Expected future date, got {value}")
        elif self.past and value > now and absolute != 0:
            raise ValueError(f"Expected past date, got {value}")

        return value
