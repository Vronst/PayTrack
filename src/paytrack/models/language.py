"""SQLAlchemy's based model for storing Currencies."""

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, validates

from ..constants.language import CODE_LENGTH, NAME_LENGTH
from ..validators import LengthValidator
from .base import Base

if TYPE_CHECKING:
    from ..validators.base import Validator


class Language(Base):
    """Language mode.

    Attributes:
    id (int): Can be skipped, due to automatically assigned.

    language_code (str): String that must not be longer than
        `paytrack.constants.language.CODE_LENGTH`.

    language_name (str): String that must not be longer than
        `paytrack.constants.language.NAME_LENGTH`.

    Methods:
        validate_name: Validates name field length.

        validate_code: Validates code field length.
    """

    __tablename__ = "languages"
    _code_validator: "Validator" = LengthValidator(max_length=CODE_LENGTH)
    _name_validator: "Validator" = LengthValidator(max_length=NAME_LENGTH)

    id: Mapped[int] = mapped_column(primary_key=True)
    language_code: Mapped[str] = mapped_column(
        String(CODE_LENGTH), unique=True, nullable=False
    )
    language_name: Mapped[str] = mapped_column(
        String(NAME_LENGTH), unique=True, nullable=False
    )

    @validates("language_name")
    def validate_name(self, key, value):
        """Validates language name.

        Uses LengthValidator to check if name
            length is acceptable.

        Args:
            key (str): Name used for error messege.
            value (str): Value to be verified.
        """
        return self._name_validator(key, value)

    @validates("language_code")
    def validate_code(self, key, value):
        """Validates language code.

        Uses LengthValidator to check if name
            length is acceptable.

        Args:
            key (str): Name used for error messege.
            value (str): Value to be verified.
        """
        return self._code_validator(key, value)
