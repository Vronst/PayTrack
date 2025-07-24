"""SQLAlchemy's based model for storing Subscriptions."""

from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, validates

from ..constants.transaction_share import MIN_AMOUNT
from ..validators import AmountValidator
from .base import Base

if TYPE_CHECKING:
    from ..validators.base import Validator


class TransactionShare(Base):
    """TransactionShare model.

    Attributes:
        id (int): Can be skipped, due to automatically assigned.

        amount (float): Float representing how much of a share was paid.
            Default to 0.0. Cannot be lower than
            `paytrack.constants.transaction_shares.MIN_AMOUNT`.

        transaction_id (int): Related transaction.

        owner_id (int): Owner's id.
    """

    __tablename__ = "transaction_shares"
    _amount_validator: "Validator" = AmountValidator(min_amount=MIN_AMOUNT)

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    transaction_id: Mapped[int] = mapped_column(
        ForeignKey("transactions.id"), nullable=False
    )
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False
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
        return self._amount_validator(key, value)
