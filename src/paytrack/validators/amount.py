"""Validators used for validating amount."""

from .base import Validator


class AmountValidator(Validator):
    """Validator that ensures a numeric amount is within defined range.

    Attributes:
        min_amount (float): Minimum allowable value - default -inf.
        max_amount (float): Maximum allowable value - default inf.
        exclusive (bool): Decides if range is exclusive or not - default True.
    """

    def __init__(
        self,
        min_amount: float = -float("inf"),
        max_amount: float = float("inf"),
        exclusive: bool = True,
    ) -> None:
        """Sets range of validation.

        Args:
            min_amount (float): default float('-inf').
            max_amount (float): default float('inf').
            exclusive (bool): if range is exclusive, default True.
        """
        self.min_amount = min_amount
        self.max_amount = max_amount
        self.exclusive = exclusive

    def __call__(self, key: str, value: float) -> float:
        """Validates the given value is within the specified range.

        Args:
            key (str): name used in error messege.
            value (float): amount to be verified.

        Raises:
            ValueError: If value is not between min_amount and maximum.
        """
        if self.exclusive:
            if not (self.min_amount < value < self.max_amount):
                raise ValueError(
                    f"{key.capitalize()} must be\
                    between {self.min_amount} and {self.max_amount}"
                )
        else:
            if not (self.min_amount <= value <= self.max_amount):
                raise ValueError(
                    f"{key.capitalize()} must be\
                    between {self.min_amount} and {self.max_amount}"
                )

        return value
