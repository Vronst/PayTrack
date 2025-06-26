from sqlalchemy import Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class TransactionShare(Base):
    __tablename__ = 'transaction_shares'

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    transaction_id: Mapped[int] = mapped_column(ForeignKey('transactions.id'), nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
