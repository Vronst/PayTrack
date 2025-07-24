import pytest  # noqa: D100

from paytrack.validators import EmailValidator


class TestPositiveEmailValidator:  # noqa: D101
    @pytest.mark.regression
    def test_email_com(self):  # noqa: D102
        validator: EmailValidator = EmailValidator()
        key: str = "test"
        email: str = "test@email.com"

        validator(key, email)

    @pytest.mark.regression
    def test_email_pl(self):  # noqa: D102
        validator: EmailValidator = EmailValidator()
        key: str = "test"
        email: str = "test@email.pl"

        validator(key, email)


class TestNegativeEmailValidator:  # noqa: D101
    def test_no_at(self):  # noqa: D102
        validator: EmailValidator = EmailValidator()
        key: str = "test"
        email: str = "testemail.com"

        with pytest.raises(ValueError):
            validator(key, email)

    def test_space_no_at(self):  # noqa: D102
        validator: EmailValidator = EmailValidator()
        key: str = "test"
        email: str = "test email.com"

        with pytest.raises(ValueError):
            validator(key, email)

    def test_no_end(self):  # noqa: D102
        validator: EmailValidator = EmailValidator()
        key: str = "test"
        email: str = "test@email"

        with pytest.raises(ValueError):
            validator(key, email)

    def test_no_start(self):  # noqa: D102
        validator: EmailValidator = EmailValidator()
        key: str = "test"
        email: str = "@email.com"

        with pytest.raises(ValueError):
            validator(key, email)

    def test_just_at(self):  # noqa: D102
        validator: EmailValidator = EmailValidator()
        key: str = "test"
        email: str = "@"

        with pytest.raises(ValueError):
            validator(key, email)

    @pytest.mark.regression
    def test_at_and_com(self):  # noqa: D102
        validator: EmailValidator = EmailValidator()
        key: str = "test"
        email: str = "@.com"

        with pytest.raises(ValueError):
            validator(key, email)

    def test_at_and_pl(self):  # noqa: D102
        validator: EmailValidator = EmailValidator()
        key: str = "test"
        email: str = "@.pl"

        with pytest.raises(ValueError):
            validator(key, email)
