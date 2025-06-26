from typing import TYPE_CHECKING
from sqlalchemy import (
    String,
    Float
)
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


if TYPE_CHECKING:
    from .transaction import Transaction


class Currency(Base):
    __tablename__ = 'currencies'

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(3), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    value: Mapped[float] = mapped_column(Float, nullable=False)

    # transactions: Mapped[list['Transaction']] = relationship(back_populates='currency')
