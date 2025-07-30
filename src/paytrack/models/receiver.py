"""SQLAlchemy's based model for storing Receivers."""

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from ..constants.receiver import NAME_LENGTH
from ..validators import LengthValidator, TypeValidator
from .associations import association_receivers
from .base import Base

if TYPE_CHECKING:
    from ..validators.base import Validator
    from .user import User


class Receiver(Base):
    """Receiver model.

    Attributes:
        id (int): Can be skipped, due to automatically assigned.

        owner_id (int): Id of related user.

        name (str): Name of receiver.

        included (list[User] | None): List of users
            that can see and use this receiver.
    """

    __tablename__ = "receivers"
    _name_validator: "Validator" = LengthValidator(max_length=NAME_LENGTH)
    _type_validator: "Validator" = TypeValidator([int])

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    included: Mapped[list["User"] | None] = relationship(
        back_populates="other_receivers",
        secondary=association_receivers,
        primaryjoin="User.id == association_receivers.c.user_id",
        secondaryjoin=id == association_receivers.c.receiver_shared_with,
    )

    @validates("name")
    def validate_name(self, key, value):
        """Validates name.

        Uses LengthValidator to check if name
            length is acceptable.

        Args:
            key (str): Name used for error messege.
            value (str): Value to be verified.
        """
        return self._name_validator(key, value)

    @validates("owner_id")
    def validate_type(self, key, value):
        """Validates types of certain fields.

        Uses TypeValidator to check if value
            is one of correct type.

        Args:
            key (str): Name used for error messege.
            value (str): Value to be verified.
        """
        return self._type_validator(key, value)
