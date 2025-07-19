"""Validators used for validaiting length of a string."""

from .base import Validator


class MaxLengthValidator(Validator):
    """Validator that ensures the max length of a string is as specified.

    Params:
        max_length (int): Maximum value length (exclusive).
    """

    def __init__(self, max_length: int):
        """Sets maximum length allowed.

        Args:
            max_length (int): maximum allowed length (exclusive).
        """
        self.max_length = max_length

    def __call__(self, key, value):
        """Validates the given value length is as specified.

        Args:
            key (str): Name used in error messsege.
            value (str): value which length will be validated.

        Raises:
            ValueError: If value exceed or meets max_length param.
        """
        try:
            if value and len(value) > self.max_length:
                raise ValueError(
                    f"{key.capitalize()} must be at\
                    most {self.max_length} characters"
                )
        except TypeError as err:
            raise TypeError(
                f"{key.capitalize()} must work with len() function"
            ) from err
        return value
