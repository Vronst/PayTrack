from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    String,
    Boolean,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .associations import association_subscription


if TYPE_CHECKING:
    from .user import User
    from .subscription_share import SubscriptionShare
    from .currency import Currency


class Subscription(Base):
    __tablename__ = 'subscriptions'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    currency_id: Mapped[int] = mapped_column(ForeignKey('currencies.id'), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    period: Mapped[str] = mapped_column(String(8), default='monthly', nullable=False)
    shared: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)

    owner: Mapped['User'] = relationship(back_populates='subscriptions')
    currency: Mapped['Currency'] = relationship()
    subscription_share: Mapped[list['SubscriptionShare']] = relationship()
    included: Mapped[list['User'] | None] = relationship(
            back_populates='included_in_subscriptions',
            secondary=association_subscription,
            primaryjoin=id == association_subscription.c.shared_with,
            secondaryjoin="User.id == association_subscription.c.user_id"
    )

