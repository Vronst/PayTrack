"""SQLAlchemy's based model for storing Savings."""

from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .associations import association_savings
from .base import Base

if TYPE_CHECKING:
    from .budget import Budget
    from .currency import Currency
    from .user import User


class Savings(Base):
    """Savings model.

    Attributes:
        id (int): Can be skipped, due to automatically assigned.

        amount (float): Float representing current balance.

        currency_id (int): Id of related currency.

        owner_id (int): Id of owner.

        included (list[User]): List of included users. These users can
            see this entry data.

        currency (Currency): Related Currency.
    """

    # TODO: make relationship with budget

    __tablename__ = "savings"

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    currency_id: Mapped[int] = mapped_column(
        ForeignKey("currencies.id"), nullable=False
    )
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

    budgets: Mapped[list["Budget"]] = relationship(back_populates="savings")
