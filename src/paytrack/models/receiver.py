from typing import TYPE_CHECKING
from sqlalchemy import (
    ForeignKey,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from ..validators import MaxLengthValidator
from .base import Base
from .associations import association_receivers
from ..constants.receiver import NAME_LENGTH


if TYPE_CHECKING:
    from .user import User
    from ..validators import Validator


class Receiver(Base):
    __tablename__ = 'receivers'
    _name_validator: 'Validator' = MaxLengthValidator(NAME_LENGTH)

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    
    included: Mapped[list['User'] | None] = relationship(
    back_populates='other_receivers',
        secondary=association_receivers,
        primaryjoin="User.id == association_receivers.c.user_id",
        secondaryjoin=id == association_receivers.c.receiver_shared_with
    )

    @validates("name")
    def validate_name(self, key, value):
        return self._name_validator(key, value)
