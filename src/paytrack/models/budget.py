"""SQLAlchemy's based model for storing Budgets."""

from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from ..constants.budget import MIN_BUDGET, PERIOD_CHOICES
from ..validators import AmountValidator, ChoiceValidator, TypeValidator
from .base import Base

if TYPE_CHECKING:
    from ..validators.base import Validator
    from .currency import Currency
    from .savings import Savings


class Budget(Base):
    """Budget model.

    Attributes:
        id (int): Can be skipped, due to automatically assigned.

        amount (float): Float describing how much money is in account.

        period (str): String that must match one of
            `paytrack.constants.budget.PERIOD_CHOICES`. Default 'monthly'

        owner_id (int): Id of owner.

        currency_id (int): Id of used currency.

        savings_id (int): Id of related savings.

        currency (Currency): Related currency.

        savings (Savings): Related savings.
    """

    __tablename__ = "budgets"
    _amount_validator: "Validator" = AmountValidator(min_amount=MIN_BUDGET)
    _period_validator: "Validator" = ChoiceValidator(PERIOD_CHOICES)
    _type_validator: "Validator" = TypeValidator([int])

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    period: Mapped[str] = mapped_column(
        String, nullable=False, default="monthly"
    )
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )
    currency_id: Mapped[int] = mapped_column(
        ForeignKey("currencies.id"), nullable=False
    )
    savings_id: Mapped[int] = mapped_column(
        ForeignKey("savings.id"), nullable=False
    )

    currency: Mapped["Currency"] = relationship()

    savings: Mapped["Savings"] = relationship(back_populates="budgets")

    @validates("amount")
    def validate_budget(self, key, value):
        """Validates budget.

        Uses AmountValidator to check if number is
            within range.

        Args:
            key (str): Name used for error messege.
            value (str): Value to be verified.
        """
        return self._amount_validator(key, value)

    @validates("period")
    def validate_period(self, key, value):
        """Validates period.

        Uses ChoiceValidator to check if value is
            in specified list.

        Args:
            key (str): Name used for error messege.
            value (str): Value to be verified.
        """
        return self._period_validator(key, value)

    @validates("owner_id", "currency_id", "savings_id")
    def validate_type(self, key, value):
        """Validates types of certain fields.

        Uses TypeValidator to check if value
            is one of correct type.

        Args:
            key (str): Name used for error messege.
            value (str): Value to be verified.
        """
        return self._type_validator(key, value)
