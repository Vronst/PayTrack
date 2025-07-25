from typing import TYPE_CHECKING
from sqlalchemy import (
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, validates
from .base import Base
from ..validators import MaxLengthValidator
from ..constants.language import NAME_LENGTH, CODE_LENGTH


if TYPE_CHECKING:
    from ..validators import Validator


class Language(Base):
    __tablename__ = "languages"
    _code_validator: 'Validator' = MaxLengthValidator(CODE_LENGTH)
    _name_validator: 'Validator' = MaxLengthValidator(NAME_LENGTH)

    id: Mapped[int] = mapped_column(primary_key=True)
    language_code: Mapped[str] = mapped_column(String(CODE_LENGTH), unique=True, nullable=False)
    language_name: Mapped[str] = mapped_column(String(NAME_LENGTH), unique=True, nullable=False)
    

    @validates("language_name")
    def validate_name(self, key, value):
        return self._name_validator(key, value)

    @validates("language_code")
    def validate_code(self, key, value):
        return self._code_validator(key, value)
