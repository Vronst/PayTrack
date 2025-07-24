"""Validators used for validating choices."""

from typing import Any

from .base import Validator


class ChoiceValidator(Validator):
    """Validates value against possible choices.

    Args:
        choice (list[Any]): list of possible choices.
    """

    def __init__(self, choice: list) -> None:
        """Sets choice as class param.

        Args:
            choice (list[Any]): list of possible choices.
        """
        self.choice = choice

    def __call__(self, key: str, value: Any) -> Any:
        """Validates given value against specified list.

        Args:
            key (str): Name used in error messege.
            value (Any): Value checked.

        Raises:
            ValueError: If value is not in specified list.
        """
        if value not in self.choice:
            raise ValueError(f"{key} must be one of {self.choice}")
        return value
