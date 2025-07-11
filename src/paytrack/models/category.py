from typing import TYPE_CHECKING
from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates 
from .base import Base 
from ..validators import MaxLengthValidator
from ..constants.category import NAME_LENGTH


if TYPE_CHECKING:
    from .translation import Translation
    from .transaction import Transaction
    from ..validators import Validator


class Category(Base):
    __tablename__ = 'categories'
    _name_validator: 'Validator' = MaxLengthValidator(NAME_LENGTH)

    id: Mapped[int] = mapped_column(primary_key=True)
    root_category: Mapped[int] = mapped_column(ForeignKey('categories.id'), nullable=True)
    custom: Mapped[bool] = mapped_column(Boolean, default=False)
    name: Mapped[str | None] = mapped_column(String(NAME_LENGTH), nullable=True)

    translations: Mapped[list['Translation']] = relationship(back_populates='categories')
    
    transactions: Mapped[list['Transaction']] = relationship(back_populates='category')

    root: Mapped['Category | None'] = relationship(
        back_populates='subcategories',
        remote_side=[id]
    )

    subcategories: Mapped[list['Category']] = relationship(back_populates='root')

    @validates("name")
    def validate_name(self, key, value):
        if not self.custom:
            raise ValueError(f'{key.capitalize()} cannot be set in non custom categories')
        return self._name_validator(key, value)
