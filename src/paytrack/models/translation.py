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

    categories: Mapped["Category"] = relationship(
        back_populates="translations"
    )

    __table_args__ = (UniqueConstraint("category_id", "language_id"),)

    @validates("word")
    def validate_word(self, key, value):
        return self._word_validator(key, value)
