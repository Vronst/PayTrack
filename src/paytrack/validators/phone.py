import re
from .base import Validator


class PhoneValidator(Validator):
    PHONE_REGEX = re.compile(r"^\+?\d+$")  # allows numbers, optional leading +

    def __call__(self, key: str, value: str) -> str:
        if not self.PHONE_REGEX.match(value):
            raise ValueError(f"{key.capitalize()} must contain only digits and optionally start with '+'")
        return value
