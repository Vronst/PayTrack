import pytest
from paytrack.validators import PinValidator 


class TestPositivePinValidator:

    def test_default(self):
        validator: PinValidator = PinValidator()
        key, value = 'test', '0134'

        validator(key, value)

    def test_length_10(self):
        validator: PinValidator = PinValidator(length=10)
        key, value = 'test', '1'*10

        validator(key, value)

    def test_length_0(self):
        validator: PinValidator = PinValidator(length=0)
        key, value = 'test', ''

        validator(key, value)


class TestNegativePinValidator:

    def test_letter(self):
        validator: PinValidator = PinValidator(length=4)
        key, value = 'test', '1a23'

        with pytest.raises(ValueError):
            validator(key, value)

    def test_too_long(self):
        validator: PinValidator = PinValidator(length=4)
        key, value = 'test', '1'*5

        with pytest.raises(ValueError):
            validator(key, value)

    def test_too_short(self):
        validator: PinValidator = PinValidator(length=4)
        key, value = 'test', '1'*3

        with pytest.raises(ValueError):
            validator(key, value)

    def test_with_space1(self):
        validator: PinValidator = PinValidator(length=4)
        key, value = 'test', '1 '*3

        with pytest.raises(ValueError):
            validator(key, value)

    def test_with_space2(self):
        validator: PinValidator = PinValidator(length=4)
        key, value = 'test', '1 23'

        with pytest.raises(ValueError):
            validator(key, value)
