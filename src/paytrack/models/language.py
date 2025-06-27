from typing import TYPE_CHECKING
from sqlalchemy import (
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, validates  # , relationship
from .base import Base
from ..validators import MaxLengthValidator


if TYPE_CHECKING:
    from ..validators import Validator


class Language(Base):
    __tablename__ = "languages"
    __code_length: int = 2
    __name_length: int = 15
    _code_validator: 'Validator' = MaxLengthValidator(__code_length)
    _name_validator: 'Validator' = MaxLengthValidator(__name_length)

    id: Mapped[int] = mapped_column(primary_key=True)
    language_code: Mapped[str] = mapped_column(String(__code_length), unique=True, nullable=False)
    language_name: Mapped[str] = mapped_column(String(__name_length), unique=True, nullable=False)
    
    # settings: Mapped[list['Setting']] = relationship(back_populates='language')

    @validates("language_name")
    def validate_name(self, key, value):
        return self._name_validator(key, value)

    @validates("language_code")
    def validate_code(self, key, value):
        return self._code_validator(key, value)
