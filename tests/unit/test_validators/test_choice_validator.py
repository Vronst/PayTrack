import pytest

from paytrack.validators.choice import ChoiceValidator


class TestPositiveChoiceValidator:

    @pytest.mark.regression
    def test_signle_choice(self):
        key: str = "test"
        choice: str = "single"
        choices: list = [choice]
        validator: ChoiceValidator = ChoiceValidator(choices)

        validator(key, choice)

    def test_signle_choice_int(self):
        key: str = "test"
        choice: int = 1
        choices: list = [choice]
        validator: ChoiceValidator = ChoiceValidator(choices)

        validator(key, choice)

    @pytest.mark.regression
    def test_multiple_choice(self):
        key: str = "test"
        choice: str = "single"
        second_choice: str = "second"
        choices: list = [choice, second_choice]
        validator: ChoiceValidator = ChoiceValidator(choices)

        validator(key, second_choice)
        validator(key, choice)

    def test_multiple_choice_any(self):
        key: str = "test"
        choice: str = "single"
        second_choice: float = 12.5
        choices: list = [choice, second_choice]
        validator: ChoiceValidator = ChoiceValidator(choices)

        validator(key, second_choice)
        validator(key, choice)


class TestNegativeChoiceValidator:

    def test_signle_choice(self):
        key: str = "test"
        choice: str = "single"
        choices: list = [choice]
        validator: ChoiceValidator = ChoiceValidator(choices)

        with pytest.raises(ValueError):
            validator(key, "1" + choice)

    @pytest.mark.regression
    def test_multiple_choice(self):
        key: str = "test"
        choice: str = "single"
        second_choice: str = "second"
        choices: list = [choice, second_choice]
        validator: ChoiceValidator = ChoiceValidator(choices)

        with pytest.raises(ValueError):
            validator(key, "1" + choice)

        with pytest.raises(ValueError):
            validator(key, "1" + second_choice)
