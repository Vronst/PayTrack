import re  # noqa: D100

import pytest

from paytrack.validators import MaxLengthValidator


class TestPositiveMaxLengthValidator:  # noqa: D101
    @pytest.mark.regression
    def test_limit(self):  # noqa: D102
        validator: MaxLengthValidator = MaxLengthValidator(max_length=2)
        key, value = "test", "a"

        validator(key, value)

    def test_limit_equal(self):  # noqa: D102
        validator: MaxLengthValidator = MaxLengthValidator(max_length=1)
        key, value = "test", "a"

        validator(key, value)


class TestNegativeMaxLengthValidator:  # noqa: D101
    @pytest.mark.regression
    def test_over_limit(self):  # noqa: D102
        validator: MaxLengthValidator = MaxLengthValidator(max_length=0)
        key, value = "test", "a"

        with pytest.raises(ValueError):
            validator(key, value)

    def test_digit(self):  # noqa: D102
        validator: MaxLengthValidator = MaxLengthValidator(max_length=10)
        key, value = "test", 1

        with pytest.raises(
            TypeError, match=re.escape("Test must work with len() function")
        ):
            validator(key, value)
