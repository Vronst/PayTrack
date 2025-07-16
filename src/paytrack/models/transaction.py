from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from ..constants.transaction import MIN_AMOUNT, TYPE_CHOICE
from ..validators import AmountValidator, ChoiceValidator, DateValidator
from .associations import association_transaction
from .base import Base

if TYPE_CHECKING:
    from ..validators import Validator
    from .category import Category
    from .currency import Currency
    from .receiver import Receiver
    from .user import User


class Transaction(Base):
    __tablename__ = "transactions"
    _amount_validator: "Validator" = AmountValidator(min_amount=MIN_AMOUNT)
    _type_validator: "Validator" = ChoiceValidator(TYPE_CHOICE)
    _date_validator: "Validator" = DateValidator()

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    done: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"), nullable=False
    )
    receiver_id: Mapped[int | None] = mapped_column(
        ForeignKey("receivers.id"), nullable=True
    )
    type: Mapped[str] = mapped_column(String(30), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    currency_id: Mapped[int] = mapped_column(
        ForeignKey("currencies.id"), nullable=False
    )
    receiver_name: Mapped[str | None] = mapped_column(
        String(50), nullable=True
    )

    owner: Mapped["User"] = relationship(back_populates="transactions")

    included: Mapped[list["User"] | None] = relationship(
        back_populates="included_in_transactions",
        secondary=association_transaction,
        primaryjoin=id == association_transaction.c.included_to_transaction,
        secondaryjoin="User.id == foreign(association_transaction.c.user_id)",
    )

    category: Mapped["Category"] = relationship(back_populates="transactions")

    currency: Mapped["Currency"] = (
        relationship()
    )  # back_populates='transactions'

    receiver: Mapped["Receiver"] = (
        relationship()
    )  # back_populates='transactions'

    @validates("type")
    def validate_type(self, key: str, value: str) -> str:
        return self._type_validator(key, value)

    @validates("amount")
    def validate_amount(self, key: str, value: float) -> float:
        return self._amount_validator(key, value)

    @validates("date")
    def validate_date(self, key, value) -> datetime:
        return self._date_validator(key, value)
