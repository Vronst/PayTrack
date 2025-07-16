from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from ..constants.subscription import (
    MIN_AMOUNT,
    NAME_LENGTH,
    PERIOD_CHOICES,
    PERIOD_LENGTH,
)
from ..validators import (
    AmountValidator,
    ChoiceValidator,
    DateValidator,
    MaxLengthValidator,
)
from .associations import association_subscription
from .base import Base

if TYPE_CHECKING:
    from ..validators import Validator
    from .currency import Currency
    from .subscription_share import SubscriptionShare
    from .user import User


class Subscription(Base):
    __tablename__ = "subscriptions"
    _name_validator: "Validator" = MaxLengthValidator(NAME_LENGTH)
    _amount_validator: "Validator" = AmountValidator(min_amount=MIN_AMOUNT)
    _period_validator: "Validator" = ChoiceValidator(PERIOD_CHOICES)
    _date_validator: "Validator" = DateValidator(future_date=True)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(NAME_LENGTH), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    currency_id: Mapped[int] = mapped_column(
        ForeignKey("currencies.id"), nullable=False
    )
    date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False
    )
    period: Mapped[str] = mapped_column(
        String(PERIOD_LENGTH), default=PERIOD_CHOICES[1], nullable=False
    )
    shared: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )

    owner: Mapped["User"] = relationship(back_populates="subscriptions")
    currency: Mapped["Currency"] = relationship()
    subscription_share: Mapped[list["SubscriptionShare"]] = relationship()
    included: Mapped[list["User"] | None] = relationship(
        back_populates="included_in_subscriptions",
        secondary=association_subscription,
        primaryjoin=id == association_subscription.c.shared_with,
        secondaryjoin="User.id == association_subscription.c.user_id",
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
