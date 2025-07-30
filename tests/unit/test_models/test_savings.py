# noqa: D100
from copy import deepcopy
from typing import Any

import pytest  # noqa: D100
from sqlalchemy.exc import IntegrityError

from paytrack.models.savings import Savings

params: list[dict] = [
    {
        "amount": 0.1,
        "currency_id": 1,
        "owner_id": 1,
    }
]

incorrect_params: list[tuple[str, Any]] = [
    ("amount", "amount"),
    ("currency_id", "currency_id"),
    ("owner_id", "owner_id"),
]


@pytest.mark.parametrize("params", params)
class TestPositiveSavings:  # noqa: D101
    @pytest.mark.regression
    def test_creation_not_full(self, session, params):  # noqa: D102
        dt = deepcopy(params)
        dt.pop("amount")

        savings: Savings = Savings(**dt)

        session.add(savings)
        session.commit()

        assert savings.amount == 0.0
        assert savings.owner_id == dt["owner_id"]
        assert savings.currency_id == dt["currency_id"]
        assert savings.budgets == []

    def test_full_creation(self, session, params):  # noqa: D102
        savings: Savings = Savings(**params)

        session.add(savings)
        session.commit()

        assert savings.amount == params["amount"]
        assert savings.owner_id == params["owner_id"]
        assert savings.currency_id == params["currency_id"]
        assert savings.budgets == []


class TestNegativeSavings:  # noqa: D101
    def test_creation_no_owner(self, session):  # noqa: D102
        currency_id: int = 1

        with pytest.raises(IntegrityError):
            result = Savings(currency_id=currency_id)
            session.add(result)
            session.commit()

    def test_creation_no_currency(self, session):  # noqa: D102
        owner_id: int = 1

        with pytest.raises(IntegrityError):
            result = Savings(owner_id=owner_id)
            session.add(result)
            session.commit()

    def test_creation_nothing(self, session):  # noqa: D102
        with pytest.raises(IntegrityError):
            result = Savings()
            session.add(result)
            session.commit()

    @pytest.mark.parametrize("data", params)
    @pytest.mark.parametrize("field, inccorect_data", incorrect_params)
    def test_incorrect_type(self, data, field, inccorect_data):  # noqa: D102
        dt = deepcopy(data)
        dt[field] = inccorect_data
        with pytest.raises(ValueError):
            Savings(**dt)
