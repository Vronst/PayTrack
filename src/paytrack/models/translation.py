"""SQLAlchemy's based model for storing Translation."""

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from ..constants.translation import WORD_LENGTH
from ..validators import LengthValidator
from .base import Base

if TYPE_CHECKING:
    from ..validators.base import Validator
    from .category import Category


class Translation(Base):
    """Translation model.

    Attributes:
        id (int): Can be skipped, due to automatically assigned.

        category_id (int): Related category's id.

        language_id (int): Related language's id.

        word (str): Translated category's name.
            Cannot be longer than
            `paytrack.constants.translations.WORD_LENGTH`.

        category (Category): Category which name is translated.
    """

    __tablename__ = "translations"
    _word_validator: "Validator" = LengthValidator(max_length=WORD_LENGTH)

    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"), nullable=False
    )
    language_id: Mapped[int] = mapped_column(
        ForeignKey("languages.id"), nullable=False
    )
    word: Mapped[str] = mapped_column(String(30), nullable=False)

    category: Mapped["Category"] = relationship(back_populates="translations")

    __table_args__ = (UniqueConstraint("category_id", "language_id"),)

    @validates("word")
    def validate_word(self, key, value):
        """Validates word field.

        Uses LengthValidator to check if value
            length is acceptable.

        Args:
            key (str): Name used for error messege.
            value (str): Value to be verified.
        """
        return self._word_validator(key, value)
