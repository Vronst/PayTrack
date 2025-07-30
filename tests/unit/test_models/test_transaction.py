from copy import deepcopy  # noqa: D100

import pytest
from sqlalchemy.exc import IntegrityError

from paytrack.constants.transaction import MIN_AMOUNT, TYPE_CHOICE
from paytrack.models import Transaction

params: list[dict] = [
    {
        "date": "1999-01-28",
        "done": True,
        "owner_id": 1,
        "category_id": 1,
        "receiver_id": 1,
        "type": TYPE_CHOICE[0],
        "amount": MIN_AMOUNT + 0.1,
        "currency_id": 1,
        "receiver_name": None,
    },
    {
        "date": "2899-11-28",
        "done": False,
        "owner_id": 2,
        "category_id": 2,
        "receiver_id": None,
        "type": TYPE_CHOICE[0],
        "amount": MIN_AMOUNT + 1.1,
        "currency_id": 2,
        "receiver_name": "Wacek",
    },
]

incorrect_params: list[tuple] = [
    ("date", "date"),
    ("done", "donw"),
    ("done", None),
    ("date", None),
    ("owner_id", "owner_id"),
    ("category_id", "category_id"),
    ("receiver_id", "receiver_id"),
    ("owner_id", 1.1),
    ("receiver_id", 1.1),
    ("category_id", 0.1),
    ("type", "incorrect_type"),
    ("type", True),
    ("amount", MIN_AMOUNT),
    ("amount", "amount"),
    ("currency_id", "currency_id"),
    ("currency_id", 0.1),
    ("receiver_name", True),
    ("receiver_name", 11),
]

missing: list[str] = [
    "owner_id",
    "category_id",
    "type",
    "amount",
    "currency_id",
]

optional: list[str] = [
    "date",
    "done",
    "receiver_id",
    "receiver_name",
]


@pytest.mark.parametrize("data", params)
class TestPositiveTransaction:  # noqa: D101
    def test_creation(self, session, data) -> None:  # noqa: D102
        result = Transaction(**data)
        session.add(result)
        session.commit()

    def test_partial_creation(self, session, data):  # noqa: D102
        dt = deepcopy(data)
        for value in optional:
            dt.pop(value)

        result = Transaction(**dt)
        session.add(result)
        session.commit()


@pytest.mark.parametrize("data", params)
class TestNegativeTransaction:  # noqa: D101
    @pytest.mark.parametrize("missing", missing)
    def test_missing_values(self, session, data, missing):  # noqa: D102
        dt = deepcopy(data)
        dt.pop(missing)

        with pytest.raises(IntegrityError):
            result = Transaction(**dt)
            session.add(result)
            session.commit()

    @pytest.mark.parametrize("field, incorrect", incorrect_params)
    def test_incorrect_params(self, session, data, field, incorrect):  # noqa: D102
        dt = deepcopy(data)
        dt[field] = incorrect

        with pytest.raises(ValueError):
            result = Transaction(**dt)
            session.add(result)
            session.commit()
