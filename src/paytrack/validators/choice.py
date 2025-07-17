from typing import Any

from . import Validator


class ChoiceValidator(Validator):
    def __init__(self, choice: list) -> None:
        self.choice = choice

    def __call__(self, key: str, value: Any) -> Any:
        if value not in self.choice:
            raise ValueError(f"{key} must be one of {self.choice}")
        return value
