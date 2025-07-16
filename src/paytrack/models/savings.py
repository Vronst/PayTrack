from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from ..constants.savings import MIN_BUDGET
from ..validators import AmountValidator
from .associations import association_savings
from .base import Base

if TYPE_CHECKING:
    from ..validators import Validator
    from .currency import Currency
    from .user import User


class Savings(Base):
    __tablename__ = "savings"
    _budget_validator: "Validator" = AmountValidator(min_amount=MIN_BUDGET)

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    currency_id: Mapped[int] = mapped_column(
        ForeignKey("currencies.id"), nullable=False
    )
    budget: Mapped[float | None] = mapped_column(Float, nullable=True)
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )

    owner: Mapped["User"] = relationship(back_populates="savings")

    included: Mapped[list["User"]] = relationship(
        back_populates="shared_savings",
        secondary=association_savings,
        primaryjoin=id == association_savings.c.shared_with,
        secondaryjoin="User.id == association_savings.c.user_id",
    )

    currency: Mapped["Currency"] = relationship()

    @validates("budget")
    def validate_budget(self, key, value):
        return self._budget_validator(key, value)
