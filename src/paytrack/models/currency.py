from typing import TYPE_CHECKING

from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column, validates

from ..constants.currency import CODE_LENGTH, NAME_LENGTH
from ..validators import MaxLengthValidator
from .base import Base

if TYPE_CHECKING:
    from ..validators import Validator


class Currency(Base):
    __tablename__ = "currencies"
    _code_validator: "Validator" = MaxLengthValidator(CODE_LENGTH)
    _name_validator: "Validator" = MaxLengthValidator(NAME_LENGTH)

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
        return self._code_validator(key, value)

    @validates("name")
    def validate_name(self, key, value):
        return self._name_validator(key, value)
