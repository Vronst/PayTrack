import re

from .base import Validator


class PinValidator(Validator):
    def __init__(self, length: int = 4) -> None:
        self.length = length
        self.pattern = re.compile(r"^\d{" + str(length) + r"}$")

    def __call__(self, key: str, value: str) -> str:
        if not self.pattern.match(value):
            raise ValueError(
                f"{key.capitalize()} must be exactly {self.length} digits"
            )
        return value
