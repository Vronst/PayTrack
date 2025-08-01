"""Validators used for valiating date."""

from datetime import UTC, date, datetime

from ..services.date import utc_now
from .base import Validator


class DateValidator(Validator):
    """Check if passed value is correct date.

    Takes two params, future_date and past_date.
    That ensures the date is either past or furute.

    Attributes:
        future_date (bool): if True, date must be later than datetime.now()
        (unless its the same day), defaults to False.

        past_date (bool): if True, date must be earlier than datetime.now()
        (unless its the same day), defaults to False.

        If both are True or both are False, no time constraint is applied.
    """

    def __init__(
        self, future_date: bool = False, past_date: bool = False
    ) -> None:
        """Sets constraints for date.

        Args:
            future_date (bool): If True,
            provided date must be later then actual. Default False.

            past_date (bool): If True,
            provided date must be earlier then actual. Default False.
        """
        if future_date and past_date:
            pass
        else:
            self.future = future_date
            self.past = past_date

    def __call__(self, key, value: str | datetime) -> datetime:
        """Validates the given value is date with set constraints.

        Args:
            key (str): Used in error messege.
            value (str | datetime): date as string or datetime class.

        Raises:
            ValueError: If value is not a date or do not meet constraints.
        """
        formats: list[str] = [
            "%d-%m-%y",
            "%d-%m-%Y",
            "%Y-%m-%d",
        ]
        if isinstance(value, str):
            value = value.strip()
            for format in formats:
                try:
                    value = datetime.strptime(value, format)
                except ValueError:
                    continue
                else:
                    break

        elif isinstance(value, date):
            value = datetime.combine(value, datetime.min.time())

        if not isinstance(value, datetime):
            raise ValueError(
                rf"{key} - Invalid datetime string format: {value}"
            )

        now = utc_now()

        if value.tzinfo is None:
            value = value.replace(tzinfo=UTC)

        absolute = abs(value - now).days

        if self.future and value < now and absolute != 0:
            raise ValueError(f"Expected future date, got {value}")
        elif self.past and value > now:
            raise ValueError(f"Expected past date, got {value}")

        return value
