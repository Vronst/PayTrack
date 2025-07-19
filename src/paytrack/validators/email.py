"""Validators used for validating emails."""

import re

from .base import Validator


class EmailValidator(Validator):
    """Validator that ensures a string is a valid email address.

    Params:
        EMAIL_REGEX (re.Pattern): pattern used for checking if email is valid.
        Should not be changed.
    """

    EMAIL_REGEX = re.compile(r"^\w+@{1}\w+\.{1}[a-z]{2,3}$")

    def __call__(self, key: str, value: str) -> str:
        """Validates the given value is a valid email address.

        Args:
            key (str): Name used in error messege.
            value (str): String that should match email pattern.

        Raises:
            ValueError: if email does not meet regex pattern.
        """
        if not self.EMAIL_REGEX.match(value):
            raise ValueError(
                f"{key.capitalize()} must be a valid email address"
            )
        return value
