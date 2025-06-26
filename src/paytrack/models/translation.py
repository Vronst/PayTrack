from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base 


class Translation(Base):
    __tablename__ = 'translations'

    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'), nullable=False)
    language_id: Mapped[int] = mapped_column(ForeignKey('languages.id'), nullable=False)
    word: Mapped[str] = mapped_column(String(30), nullable=False)

    __table_args__ = (
            UniqueConstraint('category_id', 'language_id'),
    )

