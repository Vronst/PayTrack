import re
from .base import Validator


class PhoneValidator(Validator):
    PHONE_REGEX = re.compile(r'^(?:\+48)?(\d{9})$')  # allows numbers, optional leading +

    def __call__(self, key: str, value: str) -> str | None:
        if value is None:
            return None

        value = value.replace(' ', '')
        if not self.PHONE_REGEX.match(value):
            raise ValueError(f"{key.capitalize()} must contain only digits and spaces, and optionally start with '+'")
        return value
