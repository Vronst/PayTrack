import pytest
from sqlalchemy.exc import IntegrityError
from paytrack.models.currency import Currency


class TestPositiveCurrency:

    def test_creation(self, session):
        code: str = 'PLN'
        name: str = "Złoty"
        currency: Currency = Currency(code=code, name=name, value=1.25)
        session.add(currency)
        session.commit()

        assert currency.code == code
        assert currency.name == name


class TestNegativeCurrency:
    def test_creation_no_code(self, session):
        name: str = "Złoty"
        value: float = 1.25
        with pytest.raises(IntegrityError):
            currency: Currency = Currency(name=name, value=value)
            session.add(currency)
            session.commit()


    def test_creation_no_name(self, session):
        code: str = 'PLN'
        value: float = 1.25
        with pytest.raises(IntegrityError):
            currency: Currency = Currency(code=code, value=value)
            session.add(currency)
            session.commit()

    def test_creation_no_value(self, session):
        code: str = 'PLN'
        name: str = "Złoty"
        with pytest.raises(IntegrityError):
            currency: Currency = Currency(code=code, name=name)
            session.add(currency)
            session.commit()

    def test_creation_nothing(self, session):
        with pytest.raises(IntegrityError):
            currency: Currency = Currency()
            session.add(currency)
            session.commit()
