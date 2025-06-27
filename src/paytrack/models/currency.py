from typing import TYPE_CHECKING
from sqlalchemy import (
    String,
    Float
)
from sqlalchemy.orm import Mapped, mapped_column, validates
from .base import Base
from ..validators import MaxLengthValidator


if TYPE_CHECKING:
    from ..validators import Validator


class Currency(Base):
    __tablename__ = 'currencies'
    __code_length: int = 3
    __name_length: int = 20
    _code_validator: 'Validator' = MaxLengthValidator(__code_length)
    _name_validator: 'Validator' = MaxLengthValidator(__name_length)

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(__code_length), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(__name_length), nullable=False, unique=True)
    value: Mapped[float] = mapped_column(Float, nullable=False)

    # transactions: Mapped[list['Transaction']] = relationship(back_populates='currency')

    @validates("code")
    def validates_code(self, key, value):
        return self._code_validator(key, value)

    @validates("name")
    def validate_name(self, key, value):
        return self._name_validator(key, value)
