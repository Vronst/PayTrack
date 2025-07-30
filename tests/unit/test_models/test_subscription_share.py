from copy import deepcopy  # noqa: D100

import pytest
from sqlalchemy.exc import IntegrityError  # noqa: D100

from paytrack.constants.subscription_share import MIN_AMOUNT
from paytrack.models.subscription_share import SubscriptionShare

params: list[dict] = [
    {
        "owner_id": 1,
        "amount": MIN_AMOUNT + 0.1,
        "subscription_id": 1,
    }
]

incorrect_params: list[tuple] = [
    ("owner_id", "owner_id"),
    ("amount", "amount"),
    ("amount", MIN_AMOUNT),
    ("subscription_id", "subscription_id"),
]


missing: list[str] = [
    "owner_id",
    "subscription_id",
]


class TestPositiveSubscriptionShare:  # noqa: D101
    @pytest.mark.regression
    def test_creation(self, session):  # noqa: D102
        user_id: int = 1
        subscription_id: int = 1

        subscription_share: SubscriptionShare = SubscriptionShare(
            owner_id=user_id, subscription_id=subscription_id
        )

        session.add(subscription_share)
        session.commit()

        assert subscription_share.amount == 0.0
        assert subscription_share.owner_id == user_id
        assert subscription_share.subscription_id == subscription_id

    @pytest.mark.parametrize("data", params)
    def test_full_creation(self, session, data):  # noqa: D102
        subscription_share: SubscriptionShare = SubscriptionShare(**data)

        session.add(subscription_share)
        session.commit()

        assert subscription_share.owner_id == data["owner_id"]
        assert subscription_share.subscription_id == data["subscription_id"]
        assert subscription_share.amount == data["amount"]


@pytest.mark.parametrize("data", params)
class TestNegativeSubscriptionShare:  # noqa: D101
    @pytest.mark.parametrize("missing", missing)
    def test_missing_fields(self, session, data, missing):  # noqa: D102
        dt = deepcopy(data)
        dt.pop(missing)

        with pytest.raises(IntegrityError):
            result = SubscriptionShare(**dt)
            session.add(result)
            session.commit()

    @pytest.mark.parametrize("field, incorrect_data", incorrect_params)
    def test_incorrect_fields(self, session, data, field, incorrect_data):  # noqa: D102
        dt = deepcopy(data)
        dt[field] = incorrect_data

        with pytest.raises(ValueError):
            result = SubscriptionShare(**dt)
            session.add(result)
            session.commit()
