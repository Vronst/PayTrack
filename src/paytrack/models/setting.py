"""SQLAlchemy's based model for storing Settings."""

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from ..constants.setting import MODE_CHOICES, MODE_LENGTH
from ..validators import ChoiceValidator
from .base import Base

if TYPE_CHECKING:
    from ..validators.base import Validator
    from .language import Language


class Setting(Base):
    """Setting model.

    Attributes:
        id (int): Can be skipped, due to automatically assigned.

        mode (str): String that must match one of the
            `paytrack.constants.setting.MODE_CHOICES'.

        language_id (int): Id of chosen language.

        owner_id (int): Id of owner.

        language (Language): Related language.
    """

    __tablename__ = "settings"
    _mode_validator: "Validator" = ChoiceValidator(MODE_CHOICES)

    id: Mapped[int] = mapped_column(primary_key=True)
    mode: Mapped[str] = mapped_column(
        String(MODE_LENGTH), default="dark", nullable=False
    )
    language_id: Mapped[int] = mapped_column(
        ForeignKey("languages.id"), nullable=False, default=1
    )
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, unique=True
    )

    language: Mapped["Language"] = relationship()  # back_populates='settings'

    @validates("mode")
    def validate_mode(self, key, value):
        """Validates mode.

        Uses ChoiceValidator to check if value
            is one of the `paytrack.constants.setting.MODE_CHOICES`.

        Args:
            key (str): Name used for error messege.
            value (str): Value to be verified.
        """
        return self._mode_validator(key, value)
