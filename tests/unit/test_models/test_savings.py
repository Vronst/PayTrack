import pytest
from sqlalchemy.exc import IntegrityError

from paytrack.models.savings import Savings


class TestPositiveSavings:

    @pytest.mark.regression
    def test_creation(self, session):
        currency_id: int = 1
        owner_id: int = 1

        savings: Savings = Savings(currency_id=currency_id, owner_id=owner_id)

        session.add(savings)
        session.commit()

        assert savings.amount == 0.0
        assert savings.budget is None
        assert savings.owner_id == owner_id
        assert savings.currency_id == currency_id

    def test_full_creation(self, session):
        currency_id: int = 1
        owner_id: int = 1
        amount: float = 0.5
        budget: float = 1.0

        savings: Savings = Savings(
            amount=amount, budget=budget, currency_id=currency_id, owner_id=owner_id
        )

        session.add(savings)
        session.commit()

        assert savings.amount == amount
        assert savings.owner_id == owner_id
        assert savings.currency_id == currency_id
        assert savings.budget == budget


class TestNegativeSavings:

    def test_creation_no_owner(self, session):
        currency_id: int = 1

        with pytest.raises(IntegrityError):
            savings: Savings = Savings(currency_id=currency_id)

            session.add(savings)
            session.commit()

    def test_creation_no_currency(self, session):
        owner_id: int = 1

        with pytest.raises(IntegrityError):
            savings: Savings = Savings(owner_id=owner_id)

            session.add(savings)
            session.commit()

    def test_creation_nothing(self, session):
        with pytest.raises(IntegrityError):
            savings: Savings = Savings()

            session.add(savings)
            session.commit()

    @pytest.mark.regression
    def test_budget_equal_zero(self, session):
        currency_id: int = 1
        owner_id: int = 1
        budget: float = 0.0

        with pytest.raises(ValueError):
            savings: Savings = Savings(
                budget=budget, currency_id=currency_id, owner_id=owner_id
            )

            session.add(savings)
            session.commit()

    def test_budget_below_zero(self, session):
        currency_id: int = 1
        owner_id: int = 1
        budget: float = -1.0

        with pytest.raises(ValueError):
            savings: Savings = Savings(
                budget=budget, currency_id=currency_id, owner_id=owner_id
            )

            session.add(savings)
            session.commit()
