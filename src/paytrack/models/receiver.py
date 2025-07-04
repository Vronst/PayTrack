from typing import TYPE_CHECKING
from sqlalchemy import (
    ForeignKey,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from ..validators import MaxLengthValidator
from .base import Base
from .associations import association_receivers


if TYPE_CHECKING:
    from .user import User
    from ..validators import Validator


class Receiver(Base):
    __tablename__ = 'receivers'
    __name_length: int = 50
    _name_validator: 'Validator' = MaxLengthValidator(__name_length)

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    
    included: Mapped[list['User'] | None] = relationship(
    back_populates='other_receivers',
        secondary=association_receivers,
        primaryjoin="User.id == association_receivers.c.user_id",
        secondaryjoin=id == association_receivers.c.receiver_shared_with
    )


    # transactions: Mapped[list['Transaction']] = relationship(back_populates='receiver')

    @validates("name")
    def validate_name(self, key, value):
        return self._name_validator(key, value)
