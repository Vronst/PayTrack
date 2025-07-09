from typing import TYPE_CHECKING
from sqlalchemy import Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, validates
from .base import Base
from ..validators import AmountValidator
from ..constants.transaction_share import MIN_AMOUNT


if TYPE_CHECKING:
    from ..validators import Validator


class TransactionShare(Base):
    __tablename__ = 'transaction_shares'
    _amount_validator: 'Validator' = AmountValidator(min_amount=MIN_AMOUNT)

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    transaction_id: Mapped[int] = mapped_column(ForeignKey('transactions.id'), nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)

    @validates("amount")
    def validate_amount(self, key, value):
        return self._amount_validator(key, value)
