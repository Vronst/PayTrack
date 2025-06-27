from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    String,
    Boolean,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from .base import Base
from .associations import association_subscription
from ..validators import (
        ChoiceValidator,
        MaxLengthValidator,
        AmountValidator,
        DateValidator,
)


if TYPE_CHECKING:
    from .user import User
    from .subscription_share import SubscriptionShare
    from .currency import Currency
    from ..validators import Validator


class Subscription(Base):
    __tablename__ = 'subscriptions'
    __name_length: int = 30
    __period_length: int = 8
    __amount_min: float = 0
    __period_choices: list[str] = ['daily', 'monthly', 'yearly']
    _name_validator: 'Validator' = MaxLengthValidator(__name_length)
    _amount_validator: 'Validator' = AmountValidator(min_amount=__amount_min)
    _period_validator: 'Validator' = ChoiceValidator(__period_choices)
    _date_validator: 'Validator' = DateValidator(future_date=True)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(__name_length), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    currency_id: Mapped[int] = mapped_column(ForeignKey('currencies.id'), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    period: Mapped[str] = mapped_column(String(__period_length), default=__period_choices[1], nullable=False)
    shared: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)

    owner: Mapped['User'] = relationship(back_populates='subscriptions')
    currency: Mapped['Currency'] = relationship()
    subscription_share: Mapped[list['SubscriptionShare']] = relationship()
    included: Mapped[list['User'] | None] = relationship(
            back_populates='included_in_subscriptions',
            secondary=association_subscription,
            primaryjoin=id == association_subscription.c.shared_with,
            secondaryjoin="User.id == association_subscription.c.user_id"
    )

    @validates("name")
    def validate_name(self, key, value):
        return self._name_validator(key, value)

    @validates("period")
    def validate_period(self, key, value):
        return self._period_validator(key, value)

    @validates("amount")
    def validate_amount(self, key, value):
        return self._amount_validator(key, value)

    @validates("date")
    def validate_date(self, key, value):
        return self._date_validator(key, value)
