from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship 
from .base import Base 


if TYPE_CHECKING:
    from .transaction import Transaction


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    root_category: Mapped[int] = mapped_column(ForeignKey('categories.id'), nullable=True)
    name: Mapped[str | None] = mapped_column(String(15), nullable=True)
    
    transactions: Mapped[list['Transaction']] = relationship(back_populates='category')

    root: Mapped['Category | None'] = relationship(
        back_populates='subcategories',
        remote_side=[id]
    )

    subcategories: Mapped[list['Category']] = relationship(back_populates='root')

