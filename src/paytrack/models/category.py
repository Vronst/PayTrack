"""SQLAlchemy's based model for storing Categories."""

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from ..constants.category import NAME_LENGTH
from ..validators import LengthValidator
from .base import Base

if TYPE_CHECKING:
    from ..validators.base import Validator
    from .transaction import Transaction
    from .translation import Translation


class Category(Base):
    """Category model."""

    __tablename__ = "categories"
    _name_validator: "Validator" = LengthValidator(max_length=NAME_LENGTH)

    id: Mapped[int] = mapped_column(primary_key=True)
    root_category: Mapped[int] = mapped_column(
        ForeignKey("categories.id"), nullable=True
    )
    custom: Mapped[bool] = mapped_column(Boolean, default=False)
    name: Mapped[str | None] = mapped_column(
        String(NAME_LENGTH), nullable=True
    )

    translations: Mapped[list["Translation"]] = relationship(
        back_populates="categories"
    )

    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="category"
    )

    root: Mapped["Category | None"] = relationship(
        back_populates="subcategories", remote_side=[id]
    )

    subcategories: Mapped[list["Category"]] = relationship(
        back_populates="root"
    )

    @validates("name")
    def validate_name(self, key: str, value: str):
        """Validates name.

        Uses LengthValidator to check if name
        length is acceptable.

        Args:
            key (str): Name used for error messege.
            value (str): Value to be verified.
        """
        if not self.custom:
            raise ValueError(
                f"{key.capitalize()} cannot be set in non custom categories"
            )
        return self._name_validator(key, value)
