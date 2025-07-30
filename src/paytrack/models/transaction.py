"""SQLAlchemy's based model for storing Transactions."""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from ..constants.receiver import NAME_LENGTH
from ..constants.transaction import MIN_AMOUNT, TYPE_CHOICE
from ..validators import (
    AmountValidator,
    ChoiceValidator,
    DateValidator,
    LengthValidator,
    TypeValidator,
)
from .associations import association_transaction
from .base import Base

if TYPE_CHECKING:
    from ..validators.base import Validator
    from .category import Category
    from .currency import Currency
    from .receiver import Receiver
    from .user import User


class Transaction(Base):
    """Transaction model.

    Attributes:
        id (int): Can be skipped, due to automatically assigned.

        date (datetime): Date of transaction. Default datetime.now(UTC).

        done (bool): Makrs if transaction has been already made.

        owner_id (int): Owner's id.

        category_id (int): Category's id.

        receiver_id (int | None): Receiver's id. Default None.

        type (str): String that must match one of
            `paytrack.constants.transaction.TYPE_CHOICE`.

        amount (float): Float that must be bigger than
            `paytrack.constants.transaction.MIN_AMOUNT`.

        currency_id (int): Related currency's id.

        receiver_name (str | None): Receiver's name. Should be None if
            receiver_id is provided. Default None.

        owner (User): Owner.

        included (list[User]): List of users that can see this transaction.

        category (Category): Related Category.

        currency (Currency): Related Currency.

        receiver (Receiver): Related Receiver.
    """

    __tablename__ = "transactions"
    _amount_validator: "Validator" = AmountValidator(min_amount=MIN_AMOUNT)
    _type_validator: "Validator" = ChoiceValidator(TYPE_CHOICE)
    _date_validator: "Validator" = DateValidator()
    _type_int_validator: "Validator" = TypeValidator([int])
    _type_float_validator: "Validator" = TypeValidator([float])
    _type_bool_validator: "Validator" = TypeValidator([bool])
    _name_validator: "Validator" = LengthValidator(max_length=NAME_LENGTH)

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
        String(NAME_LENGTH), nullable=True
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
        """Validates type.

        Uses ChoiceValidator to check if value
            is in specified list.

        Args:
            key (str): Name used for error messege.
            value (str): Value to be verified.
        """
        return self._type_validator(key, value)

    @validates("amount")
    def validate_amount(self, key: str, value: float) -> float:
        """Validates amount.

        Uses AmountValidator to check if value
            is in acceptable range.

        Args:
            key (str): Name used for error messege.
            value (str): Value to be verified.
        """
        self._type_float_validator(key, value)
        return self._amount_validator(key, value)

    @validates("date")
    def validate_date(self, key, value) -> datetime:
        """Validates date.

        Uses DateValidator to validate date and its format.

        Args:
            key (str): Name used for error messege.
            value (str): Value to be verified.
        """
        return self._date_validator(key, value)

    @validates("owner_id", "category_id", "receiver_id", "currency_id")
    def validate_id_type(self, key, value):
        """Validates types of certain fields.

        Uses TypeValidator to check if value
            is one of correct type.

        Args:
            key (str): Name used for error messege.
            value (str): Value to be verified.
        """
        return self._type_int_validator(key, value)

    @validates("done")
    def validate_bool_type(self, key, value):
        """Validates types of certain fields.

        Uses TypeValidator to check if value
            is one of correct type.

        Args:
            key (str): Name used for error messege.
            value (str): Value to be verified.
        """
        return self._type_bool_validator(key, value)

    @validates("receiver_name")
    def validate_name(self, key, value):
        """Validates length of field.

        Uses LengthValidator to check if value
            length is in correct range

        Args:
            key (str): Name used for error messege.
            value (str): Value to be verified.
        """
        return self._name_validator(key, value)
