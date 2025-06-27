from .base import Validator


class MaxLengthValidator(Validator):
    """
        Validates when called if length of passed value is lower then specified.

        Params:
            max_length (int): Maximum value length (exclusive).
    """
    def __init__(self, max_length: int):
        self.max_length = max_length

    def __call__(self, key, value):
        if value and len(value) > self.max_length:
            raise ValueError(f"{key.capitalize()} must be at most {self.max_length} characters")
        return value

