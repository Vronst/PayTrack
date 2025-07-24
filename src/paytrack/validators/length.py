"""Validators used for validaiting length of a string."""

from .base import Validator


class LengthValidator(Validator):
    """Validator that ensures the length of a string is as specified.

    Attributes:
        min_length (int): Minimum length (inclusive), default 1.
        max_length (int): Maximum length (exclusive), default 1.
    """

    def __init__(self, min_length: int = 1, max_length: int = 1):
        """Sets maximum length allowed.

        Args:
            min_length (int): minimum allowed length (inclusive)
            max_length (int): maximum allowed length (exclusive).
        """
        self.max_length = max_length
        self.min_length = min_length

    def __call__(self, key, value):
        """Validates the given value length is as specified.

        Args:
            key (str): Name used in error messsege.
            value (str): value which length will be validated.

        Raises:
            ValueError: If value exceed or meets max_length param.
        """
        try:
            if len(value) > self.max_length or len(value) < self.min_length:
                raise ValueError(
                    f"{key.capitalize()} must be at\
                    most {self.max_length} characters"
                )
        except TypeError as err:
            raise TypeError(
                f"{key.capitalize()} must work with len() function"
            ) from err
        return value
