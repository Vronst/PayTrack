"""Validators used to check if type of value is correct."""

from .base import Validator


class TypeValidator(Validator):
    """Validator that ensures value is of specified type.

    Attributes:
        types (list[type]): List of types the value should be of.
    """

    def __init__(self, types: list[type]) -> None:
        """Sets type for validation.

        Args:
            types (list[type]): List of types the value should be of.

        Returns:
            None
        """
        self.types = types

    def __call__(self, key: str, value: object) -> object:
        """Validates the given value is of specified type.

        Args:
                key (str): Name used in error messege.
                value (object): Value to be checked.

        Returns:
        (object): Value that was passed to it and verified.

        Raises:
        ValueError: If value is of different type.
        """
        for possibility in self.types:
            if isinstance(value, possibility):
                return value

        raise ValueError(
            f"{key}: Value should be of type {self.types},"
            f" and not {type(value)}."
        )
