import pytest  # noqa: D100
from sqlalchemy.exc import IntegrityError

from paytrack.models.subscription_share import SubscriptionShare


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

    def test_full_creation(self, session):  # noqa: D102
        user_id: int = 1
        subscription_id: int = 1
        amount: float = 10.5

        subscription_share: SubscriptionShare = SubscriptionShare(
            owner_id=user_id, subscription_id=subscription_id, amount=amount
        )

        session.add(subscription_share)
        session.commit()

        assert subscription_share.owner_id == user_id
        assert subscription_share.subscription_id == subscription_id
        assert subscription_share.amount == amount


class TestNegativeSubscriptionShare:  # noqa: D101
    def test_no_owner(self, session):  # noqa: D102
        subscription_id: int = 1
        amount: float = 10.5

        with pytest.raises(IntegrityError):
            subscription_share: SubscriptionShare = SubscriptionShare(
                subscription_id=subscription_id, amount=amount
            )

            session.add(subscription_share)
            session.commit()

    def test_no_subscription_id(self, session):  # noqa: D102
        user_id: int = 1
        amount: float = 10.5

        with pytest.raises(IntegrityError):
            subscription_share: SubscriptionShare = SubscriptionShare(
                owner_id=user_id, amount=amount
            )

            session.add(subscription_share)
            session.commit()

    def test_incorrect_amount(self, session):  # noqa: D102
        user_id: int = 1
        subscription_id: int = 1
        amount: float = -1.0

        with pytest.raises(ValueError):
            subscription_share: SubscriptionShare = SubscriptionShare(
                owner_id=user_id,
                subscription_id=subscription_id,
                amount=amount,
            )

            session.add(subscription_share)
            session.commit()
