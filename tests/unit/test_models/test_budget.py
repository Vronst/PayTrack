from copy import deepcopy  # noqa: D100
from typing import Any

import pytest
from sqlalchemy.exc import IntegrityError

from paytrack.constants.budget import MIN_BUDGET, PERIOD_CHOICES
from paytrack.models.budget import Budget

params: list[dict[str, Any]] = [
    {
        "amount": MIN_BUDGET + 0.1,
        "period": PERIOD_CHOICES[0],
        "owner_id": 1,
        "currency_id": 1,
        "savings_id": 1,
    }
]

incorrect_params: list[tuple[str, Any]] = [
    ("amount", MIN_BUDGET - 0.1),
    ("period", "Incorrect"),
    ("owner_id", "owner_id"),
    ("currency_id", "currency_id"),
    ("savings_id", "savings_id"),
]

missing: list[str] = [
    "amount",
    "owner_id",
    "currency_id",
    "savings_id",
]


@pytest.mark.parametrize("data", params)
class TestPositiveBudget:  # noqa: D101
    def test_creation(self, session, data):  # noqa: D102
        budget: Budget = Budget(**data)

        session.add(budget)
        session.commit()

        assert budget.amount == data["amount"]
        assert budget.period == data["period"]
        assert budget.owner_id == data["owner_id"]
        assert budget.currency_id == data["currency_id"]
        assert budget.savings is None
        assert budget.currency is None


@pytest.mark.parametrize("data", params)
class TestNegativeBudget:  # noqa: D101
    @pytest.mark.parametrize("field, invalid_data", incorrect_params)
    def test_creation_incorrect_data(self, session, data, field, invalid_data):  # noqa: D102
        dt = deepcopy(data)
        dt[field] = invalid_data

        with pytest.raises(ValueError):
            budget: Budget = Budget(**dt)
            session.add(budget)
            session.commit()

    @pytest.mark.parametrize("field", missing)
    def test_creation_missing_data(self, session, data, field):  # noqa: D102
        dt = deepcopy(data)
        dt.pop(field)

        with pytest.raises(IntegrityError):
            budget: Budget = Budget(**dt)
            session.add(budget)
            session.commit()
