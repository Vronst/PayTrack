from copy import deepcopy  # noqa: D100
from typing import Any

import pytest
from sqlalchemy.exc import IntegrityError

from paytrack.constants.user import PIN_LENGTH
from paytrack.models import User

params: list[dict[str, Any]] = [
    {
        "company": True,
        "name": "The TestCompany",
        "surname": None,
        "email": "example@example.com",
        "phone": "999 999 999",
        "password": "secretpass",
        "pin": "1" * PIN_LENGTH,
        "premium": False,
        "parent_id": None,
    },
    {
        "company": False,
        "name": "Simple User",
        "surname": None,
        "email": "example@example.com",
        "phone": "+48 999 999 999",
        "password": "secretpass",
        "pin": "9" * PIN_LENGTH,
        "premium": True,
        "parent_id": None,
    },
    {
        "company": True,
        "name": "MyCompany",
        "surname": None,
        "email": "example@gmail.com",
        "phone": "999999999",
        "password": "secretpass",
        "pin": "2" * PIN_LENGTH,
        "premium": False,
        "parent_id": 111,
    },
    {
        "company": False,
        "name": "Test",
        "surname": "User",
        "email": "myemail@gmail.com",
        "phone": "+48999999999",
        "password": "secretpass",
        "pin": "3" * PIN_LENGTH,
        "premium": True,
        "parent_id": 222,
    },
    {
        "company": False,
        "name": "Test",
        "surname": None,
        "email": "myemail@gmail.pl",
        "phone": None,
        "password": "secretpass",
        "pin": "3" * PIN_LENGTH,
        "premium": True,
        "parent_id": 222,
    },
]

missing: list[str] = [
    "name",
    "email",
    "password",
    "pin",
]

incorrect_params: list[tuple[str, Any]] = [
    ("company", "company"),
    ("name", 1),
    ("name", None),
    ("email", "notmyemail"),
    ("email", "email@email"),
    ("email", "email@email."),
    ("email", "@gmail.com"),
    ("email", "myemail_gmail.com"),
    ("password", 123),
    ("password", None),
    ("premium", "premium"),
]

optional: list[str] = [
    "surname",
    "phone",
    "parent_id",
]


@pytest.mark.parametrize("params", params)
class TestPositiveUser:  # noqa: D101
    def test_creation(self, session, params):  # noqa: D102
        result: User = User(**params)

        session.add(result)
        session.commit()

        assert result.name == params["name"]
        assert result.surname == params["surname"]
        assert result.company == params["company"]
        assert result.email == params["email"]
        assert result.phone == (
            params["phone"].replace(" ", "") if params["phone"] else None
        )
        assert result.password == params["password"]
        assert result.pin == params["pin"]
        assert result.premium == params["premium"]
        assert result.parent_id == params["parent_id"]
        # assert result.parent is None
        assert result.subaccounts == []
        assert result.included == []
        assert result.included_in == []
        assert result.settings is None
        assert result.transactions == []
        assert result.included_in_transactions == []
        assert result.other_receivers == []
        assert result.savings is None
        assert result.shared_savings == []
        assert result.subscriptions == []
        assert result.subscription_shares == []
        assert result.included_in_subscriptions == []
        assert result.transactions_shares == []

    def test_partial_creation(self, session, params):  # noqa: D102
        dt = deepcopy(params)
        for field in optional:
            dt.pop(field)

        result: User = User(**dt)

        session.add(result)
        session.commit()

    @pytest.mark.regression
    def test_included_relationship(self, session, users, params) -> None:  # noqa: D102
        u1, u2, u3 = users

        u1.included.extend([u2, u3])

        session.add_all([u1, u2, u3])
        session.commit()

        assert u2 in u1.included
        assert u3 in u1.included

        assert u1 in u2.included_in
        assert u1 in u3.included_in

        assert u2.included == []
        assert u3.included == []

    @pytest.mark.regression
    def test_parent_and_child(self, session, users, params) -> None:  # noqa: D102
        u1, u2, u3 = users

        session.add_all([u1, u2, u3])
        session.commit()
        assert u1.subaccounts == []
        u2.parent_id = u1.id
        session.add(u2)
        session.commit()
        assert u1.subaccounts == [u2]

        u3.parent_id = u2.id
        session.add(u3)
        session.commit()

        assert u1.parent is None
        assert len(u1.subaccounts) == 1
        assert u2.subaccounts == [u3]
        assert u3.parent == u2


@pytest.mark.parametrize("params", params)
class TestNegativeUser:  # noqa: D101
    @pytest.mark.parametrize("field", missing)
    def test_missing_data(self, session, params, field):  # noqa: D102
        dt = deepcopy(params)
        dt.pop(field)

        with pytest.raises(IntegrityError):
            result = User(**dt)
            session.add(result)
            session.commit()

    @pytest.mark.parametrize("field, incorrect", incorrect_params)
    def test_incorrect_values(self, session, params, field, incorrect):  # noqa: D102
        dt = deepcopy(params)
        dt[field] = incorrect

        with pytest.raises(ValueError):
            result = User(**dt)
            session.add(result)
            session.commit()
