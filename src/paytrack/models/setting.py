from typing import TYPE_CHECKING
from sqlalchemy import (
    ForeignKey,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from .base import Base
from ..validators import ChoiceValidator
from ..constants.setting import MODE_CHOICES, MODE_LENGTH


if TYPE_CHECKING:
    from .language import Language
    from ..validators import Validator


class Setting(Base):
    __tablename__ = "settings"
    _mode_validator: 'Validator' = ChoiceValidator(MODE_CHOICES)

    id: Mapped[int] = mapped_column(primary_key=True)
    mode: Mapped[str] = mapped_column(String(MODE_LENGTH), default='dark', nullable=False)
    language_id: Mapped[int] = mapped_column(ForeignKey("languages.id"), nullable=False, default=1)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, unique=True)


    language: Mapped['Language'] = relationship()  # back_populates='settings'

    @validates("mode")
    def validate_mode(self, key, value):
        return self._mode_validator(key, value)

