"""SQLAlchemy's based model for storing Currencies."""

from typing import TYPE_CHECKING

from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column, validates

from ..constants.currency import CODE_LENGTH, NAME_LENGTH
from ..validators import LengthValidator
from .base import Base

if TYPE_CHECKING:
    from ..validators.base import Validator


class Currency(Base):
    """Currency model."""

    __tablename__ = "currencies"
    _code_validator: "Validator" = LengthValidator(max_length=CODE_LENGTH)
    _name_validator: "Validator" = LengthValidator(max_length=NAME_LENGTH)

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(
        String(CODE_LENGTH), nullable=False, unique=True
    )
    name: Mapped[str] = mapped_column(
        String(NAME_LENGTH), nullable=False, unique=True
    )
    value: Mapped[float] = mapped_column(Float, nullable=False)

    @validates("code")
    def validates_code(self, key, value):
        """Validates Code field.

        Uses LengthValidator to check if code length is
        as expected.

        Args:
            key (str): Named used for error messege.
            value (str): Value to be checked.
        """
        return self._code_validator(key, value)

    @validates("name")
    def validate_name(self, key, value):
        """Validates Name field.

        Uses LengthValidator to check if code length is
        as expected.

        Args:
            key (str): Named used for error messege.
            value (str): Value to be checked.
        """
        return self._name_validator(key, value)
