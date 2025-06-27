import re 

from .base import Validator


class EmailValidator(Validator):
    EMAIL_REGEX = re.compile(r"^[^@]+@[^@]+\.[^@]+$")

    def __call__(self, key: str, value: str) -> str:
        if not self.EMAIL_REGEX.match(value):
            raise ValueError(f"{key.capitalize()} must be a valid email address")
        return value
