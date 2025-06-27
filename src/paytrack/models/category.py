from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates 
from .base import Base 
from ..validators import MaxLengthValidator


if TYPE_CHECKING:
    from .transaction import Transaction
    from ..validators import Validator


class Category(Base):
    __tablename__ = 'categories'
    __name_length: int = 15
    _name_validator: 'Validator' = MaxLengthValidator(__name_length)

    id: Mapped[int] = mapped_column(primary_key=True)
    root_category: Mapped[int] = mapped_column(ForeignKey('categories.id'), nullable=True)
    name: Mapped[str | None] = mapped_column(String(__name_length), nullable=True)
    
    transactions: Mapped[list['Transaction']] = relationship(back_populates='category')

    root: Mapped['Category | None'] = relationship(
        back_populates='subcategories',
        remote_side=[id]
    )

    subcategories: Mapped[list['Category']] = relationship(back_populates='root')

    @validates("name")
    def validate_name(self, key, value):
        return self._name_validator(key, value)
