"""SQLAlchemy's based model for storing SubscriptionShares."""

from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, validates

from ..constants.subscription_share import MIN_AMOUNT
from ..validators import AmountValidator, TypeValidator
from .base import Base

if TYPE_CHECKING:
    from ..validators.base import Validator


class SubscriptionShare(Base):
    """SubscriptionShare model.

    Attributes:
        id (int): Can be skipped, due to automatically assigned.

        amount (float): Float that must be higher then
            `paytrack.constants.subscription_share.MIN_AMOUNT`.

        owner_id (int): Owner id.

        subscription_id (int): subscription id.
    """

    __tablename__ = "subscription_shares"
    _amount_validator: "Validator" = AmountValidator(min_amount=MIN_AMOUNT)
    _type_validator: "Validator" = TypeValidator([int])
    _type_float_validator: "Validator" = TypeValidator([float])

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )
    subscription_id: Mapped[int] = mapped_column(
        ForeignKey("subscriptions.id"), nullable=False
    )

    @validates("amount")
    def validate_amount(self, key, value):
        """Validates amount.

        Uses AmountValidator to check if value
            is in acceptable range.

        Args:
            key (str): Name used for error messege.
            value (str): Value to be verified.
        """
        self._type_float_validator(key, value)
        return self._amount_validator(key, value)

    @validates("owner_id", "subscription_id")
    def validate_type(self, key, value):
        """Validates types of certain fields.

        Uses TypeValidator to check if value
            is one of correct type.

        Args:
            key (str): Name used for error messege.
            value (str): Value to be verified.
        """
        return self._type_validator(key, value)
