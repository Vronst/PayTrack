import pytest  # noqa: D100
from sqlalchemy.exc import IntegrityError

from paytrack.models.currency import Currency


class TestPositiveCurrency:  # noqa: D101
    def test_creation(self, session):  # noqa: D102
        code: str = "PLN"
        name: str = "Złoty"
        currency: Currency = Currency(code=code, name=name, value=1.25)
        session.add(currency)
        session.commit()

        assert currency.code == code
        assert currency.name == name


class TestNegativeCurrency:  # noqa: D101
    def test_creation_no_code(self, session):  # noqa: D102
        name: str = "Złoty"
        value: float = 1.25
        with pytest.raises(IntegrityError):
            currency: Currency = Currency(name=name, value=value)
            session.add(currency)
            session.commit()

    def test_creation_no_name(self, session):  # noqa: D102
        code: str = "PLN"
        value: float = 1.25
        with pytest.raises(IntegrityError):
            currency: Currency = Currency(code=code, value=value)
            session.add(currency)
            session.commit()

    def test_creation_no_value(self, session):  # noqa: D102
        code: str = "PLN"
        name: str = "Złoty"
        with pytest.raises(IntegrityError):
            currency: Currency = Currency(code=code, name=name)
            session.add(currency)
            session.commit()

    def test_creation_nothing(self, session):  # noqa: D102
        with pytest.raises(IntegrityError):
            currency: Currency = Currency()
            session.add(currency)
            session.commit()
