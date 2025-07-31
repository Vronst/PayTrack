from copy import deepcopy  # noqa: D100
from typing import Any

import pytest
from sqlalchemy.exc import IntegrityError

from paytrack.constants.transaction_share import MIN_AMOUNT
from paytrack.models import TransactionShare

params: list[dict[str, Any]] = [
    {"amount": MIN_AMOUNT, "transaction_id": 1, "owner_id": 1}
]

missing: list[str] = [
    "transaction_id",
    "owner_id",
]

incorrect_params: list[tuple[str, Any]] = [
    ("amount", "amount"),
    ("amount", MIN_AMOUNT - 0.1),
    ("transaction_id", "transaction_id"),
    ("owner_id", "owner_id"),
]


@pytest.mark.parametrize("params", params)
class TestPositiveTransactionShare:  # noqa: D101
    def test_creation(self, session, params):  # noqa: D102
        result: TransactionShare = TransactionShare(**params)
        session.add(result)
        session.commit()

        assert result.amount == params["amount"]
        assert result.transaction_id == params["transaction_id"]
        assert result.owner_id == params["owner_id"]

    def test_partial_creation(self, session, params):  # noqa: D102
        dt = deepcopy(params)
        dt.pop("amount")

        result: TransactionShare = TransactionShare(**dt)
        session.add(result)
        session.commit()

        assert result.amount == MIN_AMOUNT
        assert result.amount == params["amount"]
        assert result.transaction_id == params["transaction_id"]
        assert result.owner_id == params["owner_id"]


@pytest.mark.parametrize("params", params)
class TestNegativeTransactionShare:  # noqa: D101
    @pytest.mark.parametrize("field", missing)
    def test_missing_params(self, session, params, field):  # noqa: D102
        dt = deepcopy(params)
        dt.pop(field)

        with pytest.raises(IntegrityError):
            result = TransactionShare(**dt)
            session.add(result)
            session.commit()

    @pytest.mark.parametrize("field, incorrect", incorrect_params)
    def test_incorrect_data(self, session, params, field, incorrect):  # noqa: D102
        dt = deepcopy(params)
        dt[field] = incorrect

        with pytest.raises(ValueError):
            result = TransactionShare(**dt)
            session.add(result)
            session.commit()
