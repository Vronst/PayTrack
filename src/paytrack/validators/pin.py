"""Validators used for validating pin."""

import re

from .base import Validator


class PinValidator(Validator):
    """Validator that ensures a pin is numeric string of specified length."""

    def __init__(self, length: int = 4) -> None:
        """Sets length of pin, assigns automatically regex pattern.

        Args:
            length (int): required length of pin, default 4.
        """
        self.length = length
        self.pattern = re.compile(r"^\d{" + str(length) + r"}$")

    def __call__(self, key: str, value: str) -> str:
        """Validates the value has required length and contains only digits.

        Args:
            key (str): Name used for error messege.
            value (str): string to be check.
        """
        if not self.pattern.match(value):
            raise ValueError(
                f"{key.capitalize()} must be exactly {self.length} digits"
            )
        return value
