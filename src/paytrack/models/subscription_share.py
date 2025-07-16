from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, validates

from ..validators import AmountValidator
from .base import Base

if TYPE_CHECKING:
    from ..validators import Validator


class SubscriptionShare(Base):
    __tablename__ = "subscription_shares"
    __amount_min: float = 0.0
    _amount_validator: "Validator" = AmountValidator(min_amount=__amount_min)

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
        return self._amount_validator(key, value)
