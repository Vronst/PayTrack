from .base import Validator


class AmountValidator(Validator):
    """Validates when called if amount is between set minimum and maximum.

    Params:
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
        self.min_amount = min_amount
        self.max_amount = max_amount
        self.exclusive = exclusive

    def __call__(self, key: str, value: float) -> float:
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
