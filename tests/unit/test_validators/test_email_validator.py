import pytest
from paytrack.validators import EmailValidator 


class TestPositiveEmailValidator:

    def test_email_com(self):
        validator: EmailValidator = EmailValidator()
        key: str = 'test'
        email: str = 'test@email.com'

        validator(key, email)

    def test_email_pl(self):
        validator: EmailValidator = EmailValidator()
        key: str = 'test'
        email: str = 'test@email.pl'

        validator(key, email)


class TestNegativeEmailValidator:

    def test_no_at(self):
        validator: EmailValidator = EmailValidator()
        key: str = 'test'
        email: str = 'testemail.com'

        with pytest.raises(ValueError):
            validator(key, email)

    def test_space_no_at(self):
        validator: EmailValidator = EmailValidator()
        key: str = 'test'
        email: str = 'test email.com'

        with pytest.raises(ValueError):
            validator(key, email)


    def test_no_end(self):
        validator: EmailValidator = EmailValidator()
        key: str = 'test'
        email: str = 'test@email'

        with pytest.raises(ValueError):
            validator(key, email)

    def test_no_start(self):
        validator: EmailValidator = EmailValidator()
        key: str = 'test'
        email: str = '@email.com'

        with pytest.raises(ValueError):
            validator(key, email)

    def test_just_at(self):
        validator: EmailValidator = EmailValidator()
        key: str = 'test'
        email: str = '@'

        with pytest.raises(ValueError):
            validator(key, email)

    def test_at_and_com(self):
        validator: EmailValidator = EmailValidator()
        key: str = 'test'
        email: str = '@.com'

        with pytest.raises(ValueError):
            validator(key, email)

    def test_at_and_pl(self):
        validator: EmailValidator = EmailValidator()
        key: str = 'test'
        email: str = '@.pl'

        with pytest.raises(ValueError):
            validator(key, email)

