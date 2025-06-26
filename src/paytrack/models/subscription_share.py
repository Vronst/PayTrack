from sqlalchemy import (
    Float,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class SubscriptionShare(Base):
    __tablename__ = 'subscription_shares'

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    subscription_id: Mapped[int] = mapped_column(ForeignKey('subscriptions.id'), nullable=False)

