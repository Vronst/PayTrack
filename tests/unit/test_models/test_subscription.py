from datetime import datetime

import pytest
from sqlalchemy.exc import IntegrityError
from paytrack.models.subscription import Subscription


class TestPositiveSubscription:

    def test_creation(self, session):
        name: str = 'testname'
        amount: float = 10.5
        currency_id: int = 1 
        owner_id: int = 1 

        subscription: Subscription = Subscription(
            name=name,
            amount=amount,
            currency_id=currency_id,
            owner_id=owner_id
        )

        session.add(subscription)
        session.commit()

        assert subscription.owner_id == owner_id 
        assert subscription.amount == amount 
        assert subscription.currency_id == currency_id 
        assert subscription.name == name 
        assert subscription.date.date() == datetime.now().date()
        assert subscription.period == 'monthly'
        assert subscription.active == True 
        assert subscription.shared == False

    def test_full_creation(self, session):
        name: str = 'testname'
        amount: float = 10.5
        currency_id: int = 1 
        owner_id: int = 1 
        period: str = 'yearly'
        shared: bool = True 
        active: bool = False 
        date: datetime = datetime.now()

        subscription: Subscription = Subscription(
            name=name,
            amount=amount,
            currency_id=currency_id,
            owner_id=owner_id,
            period=period,
            active=active,
            shared=shared,
            date=date
        )

        session.add(subscription)
        session.commit()

        assert subscription.owner_id == owner_id 
        assert subscription.amount == amount 
        assert subscription.currency_id == currency_id 
        assert subscription.name == name 
        assert subscription.date.date() == date.date()
        assert subscription.period == period
        assert subscription.active == active
        assert subscription.shared == shared


class TestNegativeSubscription:

    def test_creation_no_name(self, session):
        amount: float = 10.5
        currency_id: int = 1 
        owner_id: int = 1 

        with pytest.raises(IntegrityError):
            subscription: Subscription = Subscription(
                amount=amount,
                currency_id=currency_id,
                owner_id=owner_id
            )

            session.add(subscription)
            session.commit()

    def test_creation_no_amount(self, session):
        name: str = 'testname'
        currency_id: int = 1 
        owner_id: int = 1 

        with pytest.raises(IntegrityError):
            subscription: Subscription = Subscription(
                name=name,
                currency_id=currency_id,
                owner_id=owner_id
            )

            session.add(subscription)
            session.commit()

    def test_creation_no_currency_id(self, session):
        name: str = 'testname'
        amount: float = 10.5
        owner_id: int = 1 

        with pytest.raises(IntegrityError):
            subscription: Subscription = Subscription(
                name=name,
                amount=amount,
                owner_id=owner_id
            )

            session.add(subscription)
            session.commit()

    def test_creation_no_owner(self, session):
        name: str = 'testname'
        amount: float = 10.5
        currency_id: int = 1 

        with pytest.raises(IntegrityError):
            subscription: Subscription = Subscription(
                name=name,
                amount=amount,
                currency_id=currency_id,
            )

            session.add(subscription)
            session.commit()

    def test_creation_nothing(self, session):

        with pytest.raises(IntegrityError):
            subscription: Subscription = Subscription()

            session.add(subscription)
            session.commit()

    def test_amount_equal_zero(self, session):
        name: str = 'testname'
        amount: float = 0.0
        currency_id: int = 1 
        owner_id: int = 1 

        with pytest.raises(ValueError):
            subscription: Subscription = Subscription(
                name=name,
                amount=amount,
                currency_id=currency_id,
                owner_id=owner_id
            )

            session.add(subscription)
            session.commit()

    def test_incorrect_period(self, session):
        name: str = 'testname'
        amount: float = 10.5
        currency_id: int = 1 
        owner_id: int = 1 
        period: str = 'neverly'

        with pytest.raises(ValueError):
            subscription: Subscription = Subscription(
                name=name,
                amount=amount,
                currency_id=currency_id,
                owner_id=owner_id,
                period=period
            )

            session.add(subscription)
            session.commit()

    def test_too_long_name(self, session):
        name: str = 't' * 31
        amount: float = 10.5
        currency_id: int = 1 
        owner_id: int = 1 

        with pytest.raises(ValueError):
            subscription: Subscription = Subscription(
                name=name,
                amount=amount,
                currency_id=currency_id,
                owner_id=owner_id
            )

            session.add(subscription)
            session.commit()

    def test_too_long_period_name(self, session):
        name: str = 'testname'
        amount: float = 10.5
        currency_id: int = 1 
        owner_id: int = 1 
        period: str = 't' * 9

        with pytest.raises(ValueError):
            subscription: Subscription = Subscription(
                name=name,
                amount=amount,
                currency_id=currency_id,
                owner_id=owner_id,
                period=period
            )

            session.add(subscription)
            session.commit()
