from copy import deepcopy  # noqa: D100
from datetime import datetime

import pytest
from sqlalchemy.exc import IntegrityError

from paytrack.constants.subscription import (
    MIN_AMOUNT,
    NAME_LENGTH,
    PERIOD_CHOICES,
)
from paytrack.models.subscription import Subscription
from paytrack.services.date import utc_now

params: list[dict] = [
    {
        "name": "testname",
        "amount": MIN_AMOUNT + 1.1,
        "currency_id": 1,
        "owner_id": 1,
        "period": PERIOD_CHOICES[0],
        "shared": True,
        "active": True,
        "date": datetime.now().date(),
    },
    {
        "name": "name",
        "amount": MIN_AMOUNT * 2 + 0.1,
        "currency_id": 2,
        "owner_id": 2,
        "period": PERIOD_CHOICES[0],
        "shared": False,
        "active": True,
        "date": datetime.now(),
    },
    {
        "name": "my_name1",
        "amount": MIN_AMOUNT * 2 + 0.1,
        "currency_id": 3,
        "owner_id": 3,
        "period": PERIOD_CHOICES[0],
        "shared": False,
        "active": False,
        "date": "3999-01-28",
    },
    {
        "name": "my_name1",
        "amount": MIN_AMOUNT * 2 + 0.1,
        "currency_id": 3,
        "owner_id": 3,
        "period": PERIOD_CHOICES[0],
        "shared": True,
        "active": False,
        "date": "3000-11-28",
    },
]

inccorect_params: list[tuple] = [
    ("name", 1),
    ("name", "a" * (NAME_LENGTH + 1)),
    ("amount", "amount"),
    ("amount", MIN_AMOUNT),
    ("currency_id", "currency_id"),
    ("owner_id", "owner_id"),
    ("period", "not_valid"),
    ("period", 1),
    ("shared", "maybe"),
    ("active", "probably"),
    ("date", "date"),
]

missing: list[str] = [
    "name",
    "amount",
    "currency_id",
    "owner_id",
]


class TestPositiveSubscription:  # noqa: D101
    def test_creation(self, session):  # noqa: D102
        name: str = "testname"
        amount: float = 10.5
        currency_id: int = 1
        owner_id: int = 1

        subscription: Subscription = Subscription(
            name=name,
            amount=amount,
            currency_id=currency_id,
            owner_id=owner_id,
        )

        session.add(subscription)
        session.commit()

        assert subscription.owner_id == owner_id
        assert subscription.amount == amount
        assert subscription.currency_id == currency_id
        assert subscription.name == name
        assert subscription.date.date() == utc_now().date()
        assert subscription.period == "monthly"
        assert subscription.active
        assert not subscription.shared

    @pytest.mark.parametrize("data", params)
    def test_full_creation(self, session, data):  # noqa: D102
        subscription: Subscription = Subscription(**data)

        session.add(subscription)
        session.commit()

        assert subscription.owner_id == data["owner_id"]
        assert subscription.amount == data["amount"]
        assert subscription.currency_id == data["currency_id"]
        assert subscription.name == data["name"]
        assert subscription.date.date()
        assert subscription.period == data["period"]
        assert subscription.active == data["active"]
        assert subscription.shared == data["shared"]


class TestNegativeSubscription:  # noqa: D101
    @pytest.mark.parametrize("data", params)
    @pytest.mark.parametrize("field, incorrect_data", inccorect_params)
    def test_inccorect_value(self, session, data, field, incorrect_data):  # noqa: D102
        dt = deepcopy(data)
        dt[field] = incorrect_data

        with pytest.raises(ValueError):
            Subscription(**dt)

    @pytest.mark.parametrize("data", params)
    @pytest.mark.parametrize("missing", missing)
    def test_missing_data(self, session, data, missing):  # noqa: D102
        dt = deepcopy(data)
        dt.pop(missing)

        with pytest.raises(IntegrityError):
            result = Subscription(**dt)
            session.add(result)
            session.commit()
