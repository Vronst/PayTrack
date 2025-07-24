"""SQLAlchemy's based model for storing Subscriptions."""

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
from ..services.date import utc_now
from ..validators import (
    AmountValidator,
    ChoiceValidator,
    DateValidator,
    LengthValidator,
)
from .associations import association_subscription
from .base import Base

if TYPE_CHECKING:
    from ..validators.base import Validator
    from .currency import Currency
    from .subscription_share import SubscriptionShare
    from .user import User


class Subscription(Base):
    """Subscription model.

    Attributes:
        id (int): Can be skipped, due to automatically assigned.

        name (str): Name of subscriptions, which length must be less than
            `paytrack.constants.subscriptions.NAME_LENGTH`.

        amount (float): How much must be paid per selected period.

        currency_id (int): Id of used currency.

        date (datetime): Date of when subscription started.
            Default datetime.now(UTC).

        period (str): String that must match one of
            `paytrack.constants.subscription.PERIOD_CHOICES`.

        shared (bool): True if users are added do included.

        active (bool): True if subscription is active.

        owner_id (int): Id of user with owner privilages.

        owner (User): Owner.

        currency (Currency): Related currency.

        subscription_share (SubscriptionShare): Related subscription payments.

        included (list[User]): Users included with this subscription.
    """

    __tablename__ = "subscriptions"
    _name_validator: "Validator" = LengthValidator(max_length=NAME_LENGTH)
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
        DateTime, default=utc_now, nullable=False
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
        """Validates name.

        Uses LengthValidator to check if name
            length is acceptable.

        Args:
            key (str): Name used for error messege.
            value (str): Value to be verified.
        """
        return self._name_validator(key, value)

    @validates("period")
    def validate_period(self, key, value):
        """Validates period.

        Uses ChoiceValidator to check if value
            is within specified list.

        Args:
            key (str): Name used for error messege.
            value (str): Value to be verified.
        """
        return self._period_validator(key, value)

    @validates("amount")
    def validate_amount(self, key, value):
        """Validates amount.

        Uses AmountValidator to check if value
            is in acceptable range.

        Args:
            key (str): Name used for error messege.
            value (str): Value to be verified.
        """
        return self._amount_validator(key, value)

    @validates("date")
    def validate_date(self, key, value):
        """Validates date.

        Uses DateValidator to validate date and its format.

        Args:
            key (str): Name used for error messege.
            value (str): Value to be verified.
        """
        return self._date_validator(key, value)
