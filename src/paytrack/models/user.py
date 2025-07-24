"""SQLAlchemy's based model for storing Users."""

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from ..constants.user import (
    EMAIL_LENGTH,
    NAME_LENGTH,
    PHONE_LENGTH,
    PIN_LENGTH,
)
from ..validators import (
    EmailValidator,
    LengthValidator,
    PhoneValidator,
    PinValidator,
)
from .associations import (
    association_included,
    association_receivers,
    association_savings,
    association_subscription,
    association_transaction,
)
from .base import Base

if TYPE_CHECKING:
    from ..validators.base import Validator
    from .receiver import Receiver
    from .savings import Savings
    from .setting import Setting
    from .subscription import Subscription
    from .subscription_share import SubscriptionShare
    from .transaction import Transaction
    from .transaction_share import TransactionShare


class User(Base):
    """User model.

    Attributes:
        id (int): Can be skipped, due to automatically assigned.

        company (bool): If True, surname is not needed.

        name (str): User's name. Cannot be longer than
            `paytrack.constants.user.NAME_LENGTH`.

        surname (str | None): User's surname. Omit if company is True.

        admin (bool): If True, user has admin privilages.

        email (str): String that contains valid email.

        phone (str | None): String containing valid phone number.
            Default None.

        password (str): User password, stored as hash.

        pin (str): User pin, stored as hash.

        premium (bool): If user bought premium.

        parent_id (int | None): User's main account id.

        parent (User): Parent account.

        subaccounts (list[User]): List of users that has this user as parent.

        included (list[User]): List of users sharing this account.

        included_in (list[User]): List of users that shared their
            acount to this one.

        settings (Setting): Related settings.

        transaction (list[Transaction]): List of transaction created by
            this user.

        included_in_transactions (list[Transaction]): List of transaction of
            other users that this user can see.

        other_receivers (list[Receiver]): List of receivers that
            this user can see and use in its transactions.

        savings (Savings): Related savings.

        shared_savings (list[Savings]): List of other users savings that
            this user can see.

        subscriptions (list[Subscription]): List of user's subscriptions.

        subscription_share (list[SubscriptionShare]): List of subscription
            shares, that this user is part of.

        included_in_subscriptions (list[Subscription]): List of subscriptions,
            shared to this user.

        transactions_shares (list[TransactionShare]): List of transaction
            shares, that this user is part of.
    """

    __tablename__ = "users"
    _name_validator: "Validator" = LengthValidator(max_length=NAME_LENGTH)
    _pin_validator: "Validator" = PinValidator(PIN_LENGTH)
    _email_validator: "Validator" = EmailValidator()
    _phone_validator: "Validator" = PhoneValidator()

    # black and flake8 were fighting over line limit besides
    # having the same one, so here is helper to make it shorter
    _association_subscription_helper: str = (
        "Subscription.id == association_subscription.c.shared_with"
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    company: Mapped[bool] = mapped_column(Boolean, default=False)
    name: Mapped[str] = mapped_column(String(NAME_LENGTH), nullable=False)
    surname: Mapped[str | None] = mapped_column(
        String(NAME_LENGTH), nullable=True
    )
    admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    email: Mapped[str] = mapped_column(
        String(EMAIL_LENGTH), unique=True, nullable=False
    )
    phone: Mapped[str | None] = mapped_column(
        String(PHONE_LENGTH), nullable=True
    )
    password: Mapped[str] = mapped_column(String, nullable=False)
    pin: Mapped[str | None] = mapped_column(String, nullable=True)
    premium: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )

    parent: Mapped["User | None"] = relationship(
        back_populates="subaccounts", remote_side=[id], lazy="selectin"
    )
    subaccounts: Mapped[list["User"]] = relationship(back_populates="parent")

    included: Mapped[list["User"]] = relationship(
        back_populates="included_in",
        secondary=association_included,
        primaryjoin=id == association_included.c.user_id,
        secondaryjoin=id == association_included.c.included_user_id,
    )
    included_in: Mapped[list["User"]] = relationship(
        back_populates="included",
        secondary=association_included,
        primaryjoin=id == association_included.c.included_user_id,
        secondaryjoin=id == association_included.c.user_id,
        lazy="selectin",
    )

    settings: Mapped["Setting"] = relationship(
        cascade="all, delete-orphan"
    )  # back_populates='owner',

    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="owner"
    )

    included_in_transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="included",
        secondary=association_transaction,
        primaryjoin=id == association_transaction.c.user_id,
        secondaryjoin=(
            "Transaction.id \
            ==\
            association_transaction.c.included_to_transaction"
        ),
    )

    other_receivers: Mapped[list["Receiver"]] = relationship(
        back_populates="included",
        secondary=association_receivers,
        primaryjoin=id == association_receivers.c.user_id,
        secondaryjoin=(
            "Receiver.id \
                ==\
                association_receivers.c.receiver_shared_with"
        ),
    )

    savings: Mapped["Savings"] = relationship(back_populates="owner")

    shared_savings: Mapped[list["Savings"]] = relationship(
        back_populates="included",
        secondary=association_savings,
        primaryjoin=id == association_savings.c.user_id,
        secondaryjoin="Savings.id == association_savings.c.shared_with",
    )

    subscriptions: Mapped[list["Subscription"]] = relationship(
        back_populates="owner"
    )

    subscription_shares: Mapped[list["SubscriptionShare"]] = relationship()
    included_in_subscriptions: Mapped[list["Subscription"]] = relationship(
        back_populates="included",
        secondary=association_subscription,
        primaryjoin=id == association_subscription.c.user_id,
        secondaryjoin=_association_subscription_helper,
    )

    transactions_shares: Mapped[list["TransactionShare"]] = relationship()

    @validates("name", "surname")
    def validate_name(self, key: str, value: str) -> str:
        """Validates name and surname.

        Uses LengthValidator to check if value
            length is acceptable.

        Args:
            key (str): Name used for error messege.
            value (str): Value to be verified.
        """
        return self._name_validator(key, value)

    @validates("pin")
    def validate_pin(self, key: str, value: str) -> str:
        """Validates pin.

        Uses PinValidator to check if value
            length is as precised and contains only digits.

        Args:
            key (str): Name used for error messege.
            value (str): Value to be verified.
        """
        return self._pin_validator(key, value)

    @validates("email")
    def validate_email(self, key: str, value: str) -> str:
        """Validates email.

        Uses EmailValidator to check if value
            is valid email.

        Args:
            key (str): Name used for error messege.
            value (str): Value to be verified.
        """
        return self._email_validator(key, value)

    @validates("phone")
    def validate_phone(self, key: str, value: str) -> str:
        """Validates phone.

        Uses PhoneValidator to check if value
            is valid phone number (with or without prefix +xx).

        Args:
            key (str): Name used for error messege.
            value (str): Value to be verified.
        """
        return self._phone_validator(key, value)

    def __repr__(self) -> str:
        """String representation of User.

        Returns:
            str
        """
        return (
            f"User(id={self.id!r},admin={self.admin!r},"
            f" name={self.name!r}, surname={self.surname!r},"
            f" email={self.email!r},"
            f"phone={self.phone!r}, password=****, company={self.company!r}, "
            f"pin=****"
        )
