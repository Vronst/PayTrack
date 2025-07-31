import pytest  # noqa: D100

from paytrack.validators import PhoneValidator


class TestPositivePhoneValidator:  # noqa: D101
    @pytest.mark.regression
    def test_phone_no_space(self):  # noqa: D102
        validator: PhoneValidator = PhoneValidator()
        phone: str = "9" * 9
        key: str = "test"

        validator(key, phone)

    def test_phone_many_spaces(self):  # noqa: D102
        validator: PhoneValidator = PhoneValidator()
        phone: str = "  9      " * 9
        key: str = "test"

        result = validator(key, phone)

        assert result == "9" * 9

    def test_phone_spaces(self):  # noqa: D102
        validator: PhoneValidator = PhoneValidator()
        phone: str = "9" * 3 + " " + "9" * 3 + " " + "9" * 3
        key: str = "test"

        validator(key, phone)

    @pytest.mark.regression
    def test_phone_spaces_and_prefix(self):  # noqa: D102
        validator: PhoneValidator = PhoneValidator()
        phone: str = "+48 " + "9" * 3 + " " + "9" * 3 + " " + "9" * 3
        key: str = "test"

        validator(key, phone)

    def test_phone_prefix(self):  # noqa: D102
        validator: PhoneValidator = PhoneValidator()
        phone: str = "+48" + "9" * 9
        key: str = "test"

        validator(key, phone)

    def test_phone_prefix_one_space(self):  # noqa: D102
        validator: PhoneValidator = PhoneValidator()
        phone: str = "+48 " + "9" * 9
        key: str = "test"

        validator(key, phone)


class TestNegativePhoneValidator:  # noqa: D101
    @pytest.mark.regression
    def test_letter(self):  # noqa: D102
        validator: PhoneValidator = PhoneValidator()
        phone: str = "+4a " + "9" * 9
        key: str = "test"

        with pytest.raises(ValueError):
            validator(key, phone)

    def test_missing_digit_in_prefix(self):  # noqa: D102
        validator: PhoneValidator = PhoneValidator()
        phone: str = "+4 " + "9" * 9
        key: str = "test"

        with pytest.raises(ValueError):
            validator(key, phone)

    def test_missing_digit_with_prefix(self):  # noqa: D102
        validator: PhoneValidator = PhoneValidator()
        phone: str = "+48" + "9" * 8
        key: str = "test"

        with pytest.raises(ValueError):
            validator(key, phone)

    @pytest.mark.regression
    def test_missing_digit(self):  # noqa: D102
        validator: PhoneValidator = PhoneValidator()
        phone: str = "9" * 8
        key: str = "test"

        with pytest.raises(ValueError):
            validator(key, phone)
