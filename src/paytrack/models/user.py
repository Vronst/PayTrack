from typing import TYPE_CHECKING
from sqlalchemy import (
    ForeignKey,
    String,
    Boolean,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .associations import (
    association_transaction,
    association_included,
    association_receivers,
)
from .transaction import Transaction


if TYPE_CHECKING:
    from .receiver import Receiver
    from .setting import Setting





class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    company: Mapped[bool] = mapped_column(Boolean, default=False)
    name: Mapped[str] = mapped_column(String(30))
    surname: Mapped[str] = mapped_column(String(30), nullable=True)
    admin: Mapped[bool] = mapped_column(Boolean, default=False)
    email: Mapped[str] = mapped_column(String(50), unique=True)
    phone: Mapped[str | None] = mapped_column(String(12), nullable=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey('users.id'), nullable=True)

    parent: Mapped["User"] = relationship(back_populates="subaccounts", remote_side=[id],
                                          lazy='selectin')
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

    settings: Mapped['Setting'] = relationship(back_populates='owner', cascade='all, delete-orphan')

    transactions: Mapped[list["Transaction"] | None] = relationship(back_populates='owner')

    included_in_transactions: Mapped[list['Transaction'] | None] = relationship(
            back_populates='included',
            secondary=association_transaction,
        primaryjoin=id == association_transaction.c.user_id,
        secondaryjoin=Transaction.id == association_transaction.c.included_to_transaction
    )

    other_receivers: Mapped[list['Receiver'] | None] = relationship(
            back_populates='included',
            secondary=association_receivers,
            primaryjoin=id == association_receivers.c.user_id,
            secondaryjoin="Receiver.id == association_receivers.c.receiver_shared_with"
    )

    def __repr__(self) -> str:
        return \
        f"User(id={self.id!r},admin={self.admin!r},"\
        f" name={self.name!r}, surname={self.surname!r}, email={self.email!r},"\
        f"phone={self.phone!r}, password=****, len(included)={len(self.included) if self.included else 'N/A'}"\
        f"included_in={self.included_in if self.included_in else 'N/A'!r}"\
        f"parent={self.parent!r}, subaccounts={self.subaccounts if self.subaccounts else 'N/A'!r}"
    
