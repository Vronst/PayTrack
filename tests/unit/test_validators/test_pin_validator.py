import pytest  # noqa: D100

from paytrack.validators import PinValidator


class TestPositivePinValidator:  # noqa: D101
    @pytest.mark.regression
    def test_default(self):  # noqa: D102
        validator: PinValidator = PinValidator()
        key, value = "test", "0134"

        validator(key, value)

    @pytest.mark.regression
    def test_length_10(self):  # noqa: D102
        validator: PinValidator = PinValidator(length=10)
        key, value = "test", "1" * 10

        validator(key, value)

    def test_length_0(self):  # noqa: D102
        validator: PinValidator = PinValidator(length=0)
        key, value = "test", ""

        validator(key, value)


class TestNegativePinValidator:  # noqa: D101
    def test_letter(self):  # noqa: D102
        validator: PinValidator = PinValidator(length=4)
        key, value = "test", "1a23"

        with pytest.raises(ValueError):
            validator(key, value)

    def test_too_long(self):  # noqa: D102
        validator: PinValidator = PinValidator(length=4)
        key, value = "test", "1" * 5

        with pytest.raises(ValueError):
            validator(key, value)

    @pytest.mark.regression
    def test_too_short(self):  # noqa: D102
        validator: PinValidator = PinValidator(length=4)
        key, value = "test", "1" * 3

        with pytest.raises(ValueError):
            validator(key, value)

    def test_with_space1(self):  # noqa: D102
        validator: PinValidator = PinValidator(length=4)
        key, value = "test", "1 " * 3

        with pytest.raises(ValueError):
            validator(key, value)

    def test_with_space2(self):  # noqa: D102
        validator: PinValidator = PinValidator(length=4)
        key, value = "test", "1 23"

        with pytest.raises(ValueError):
            validator(key, value)
