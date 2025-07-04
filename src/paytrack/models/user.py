from typing import TYPE_CHECKING
from sqlalchemy import (
    ForeignKey,
    String,
    Boolean,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from .base import Base
from .associations import (
    association_transaction,
    association_included,
    association_receivers,
    association_savings,
    association_subscription,
)
from ..validators import (
        MaxLengthValidator,
        PhoneValidator,
        EmailValidator,
        PinValidator
)


if TYPE_CHECKING:
    from .receiver import Receiver
    from .setting import Setting
    from .transaction import Transaction
    from .savings import Savings
    from .subscription import Subscription
    from .subscription_share import SubscriptionShare
    from .transaction_share import TransactionShare
    from ..validators import Validator


class User(Base):
    __tablename__ = 'users'
    __name_length: int = 30
    __pin_length: int = 6
    _name_validator: 'Validator' = MaxLengthValidator(__name_length)
    _pin_validator: 'Validator' = PinValidator(__pin_length)
    _email_validator: 'Validator' = EmailValidator()
    _phone_validator: 'Validator' = PhoneValidator()

    id: Mapped[int] = mapped_column(primary_key=True)
    company: Mapped[bool] = mapped_column(Boolean, default=False)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    surname: Mapped[str | None] = mapped_column(String(30), nullable=True)
    admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    phone: Mapped[str | None] = mapped_column(String(12), nullable=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    pin: Mapped[str | None] = mapped_column(String(6), nullable=True)
    premium: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey('users.id'), nullable=True)

    parent: Mapped["User | None"] = relationship(back_populates="subaccounts", remote_side=[id], lazy='selectin')
    subaccounts: Mapped[list['User']] = relationship(
            back_populates='parent'
    )

    included: Mapped[list["User"]] = relationship(
            back_populates='included_in',
            secondary=association_included,
            primaryjoin=id == association_included.c.user_id,
            secondaryjoin=id == association_included.c.included_user_id
    )
    included_in: Mapped[list["User"]] = relationship(
            back_populates='included',
            secondary=association_included,
            primaryjoin=id ==association_included.c.included_user_id,
            secondaryjoin=id == association_included.c.user_id,
            lazy='selectin'
    )

    settings: Mapped['Setting'] = relationship(cascade='all, delete-orphan')  # back_populates='owner', 

    transactions: Mapped[list["Transaction"]] = relationship(back_populates='owner')

    included_in_transactions: Mapped[list['Transaction']] = relationship(
            back_populates='included',
            secondary=association_transaction,
        primaryjoin=id == association_transaction.c.user_id,
        secondaryjoin="Transaction.id == association_transaction.c.included_to_transaction"
    )

    other_receivers: Mapped[list['Receiver']] = relationship(
            back_populates='included',
            secondary=association_receivers,
            primaryjoin=id == association_receivers.c.user_id,
            secondaryjoin="Receiver.id == association_receivers.c.receiver_shared_with"
    )

    savings: Mapped['Savings'] = relationship(back_populates='owner')

    shared_savings: Mapped[list['Savings']] = relationship(
        back_populates='included',
        secondary=association_savings,
        primaryjoin=id == association_savings.c.user_id,
        secondaryjoin='Savings.id == association_savings.c.shared_with'
    )

    subscriptions: Mapped[list['Subscription']] = relationship(back_populates='owner')

    subscription_shares: Mapped[list['SubscriptionShare']] = relationship()
    included_in_subscriptions: Mapped[list['Subscription']] = relationship(
        back_populates='included',
        secondary=association_subscription,
        primaryjoin=id == association_subscription.c.user_id,
        secondaryjoin="Subscription.id == association_subscription.c.shared_with"
    )

    transactions_shares: Mapped[list['TransactionShare']] = relationship()

    @validates("name", "surname")
    def validate_name(self, key: str, value: str) -> str:
        return self._name_validator(key, value)

    @validates("pin")
    def validate_pin(self, key: str, value: str) -> str:
        return self._pin_validator(key, value)

    @validates("email")
    def validate_email(self, key: str, value: str) -> str:
        return self._email_validator(key, value)

    @validates("phone")
    def validate_phone(self, key: str, value: str) -> str:
        return self._phone_validator(key, value)

    def __repr__(self) -> str:
        return \
        f"User(id={self.id!r},admin={self.admin!r},"\
        f" name={self.name!r}, surname={self.surname!r}, email={self.email!r},"\
        f"phone={self.phone!r}, password=****, company={self.company!r}, "\
        f"pin=****"
    
