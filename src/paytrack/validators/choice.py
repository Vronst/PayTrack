from . import Validator 


class ChoiceValidator(Validator):

    def __init__(self, choice: list) -> None:
        self.choice = choice

    def __call__(self, key: str, value: str | int | float) -> str | int | float:
        if value not in self.choice:
            raise ValueError(f"{key.capitalize()} must be one of {self.choice}")
        return value

