import re
import pytest
from paytrack.validators import MaxLengthValidator 


class TestPositiveMaxLengthValidator:

    def test_limit(self):
        validator: MaxLengthValidator = MaxLengthValidator(
                max_length=2
        )
        key, value = 'test', 'a'

        validator(key, value)

    def test_limit_equal(self):
        validator: MaxLengthValidator = MaxLengthValidator(
                max_length=1
        )
        key, value = 'test', 'a'

        validator(key, value)

class TestNegativeMaxLengthValidator:

    def test_over_limit(self):
        validator: MaxLengthValidator = MaxLengthValidator(
                max_length=0
        )
        key, value = 'test', 'a'

        with pytest.raises(ValueError):
            validator(key, value)

    def test_digit(self):
        validator: MaxLengthValidator = MaxLengthValidator(
                max_length=10
        )
        key, value = 'test', 1

        with pytest.raises(TypeError, match=re.escape('Test must work with len() function')):
            validator(key, value)
