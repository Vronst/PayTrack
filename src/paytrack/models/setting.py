from typing import TYPE_CHECKING
from sqlalchemy import (
    ForeignKey,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from .base import Base
from ..validators import ChoiceValidator


if TYPE_CHECKING:
    from .language import Language
    from ..validators import Validator


class Setting(Base):
    __tablename__ = "settings"
    __mode_length: int = 15
    __type_length: int = 15
    __mode_choices: list[str] = ['dark', 'light']
    __type_choices: list[str] = ['standard', 'elastic']
    _mode_validator: 'Validator' = ChoiceValidator(__mode_choices)
    _type_validator: 'Validator' = ChoiceValidator(__type_choices)

    id: Mapped[int] = mapped_column(primary_key=True)
    mode: Mapped[str] = mapped_column(String(__mode_length), default='dark', nullable=False)
    language_id: Mapped[int] = mapped_column(ForeignKey("languages.id"), nullable=False, default=1)
    type: Mapped[str] = mapped_column(String(__type_length), default="standard")
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, unique=True)

    # owner: Mapped['User'] = relationship(back_populates='settings', single_parent=True)

    language: Mapped['Language'] = relationship()  # back_populates='settings'

    @validates("mode")
    def validate_mode(self, key, value):
        return self._mode_validator(key, value)

    @validates("type")
    def validate_type(self, key, value):
        return self._type_validator(key, value)
            
