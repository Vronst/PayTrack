"""Validators used for validating phone numebers."""

import re

from .base import Validator


class PhoneValidator(Validator):
    """Validator that ensures a string is a valid phone number.

    Phone number can be provided either with or without prefix.

    Attributes:
        PHONE_REGEX (re.Pattern): regex patter to verify phone numbers.
        THAT SHOULD NOT BE CHANGED.
    """

    PHONE_REGEX = re.compile(
        r"^(?:\+48)?(\d{9})$"
    )  # allows numbers, optional leading +

    def __call__(self, key: str, value: str) -> str | None:
        """Validates the given value is phone number.

        Args:
            key (str): Name used in error messege.

            value (str): string containing valid phone number.
            With or without prefix.

        Raises:
            ValueError: if string does not meet regex pattern.
        """
        if value is None:
            return None

        value = value.replace(" ", "")
        if not self.PHONE_REGEX.match(value):
            raise ValueError(
                f"{key.capitalize()} must contain only digits\
                and spaces, and optionally start with '+'"
            )
        return value
