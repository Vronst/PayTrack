from typing import TYPE_CHECKING
from sqlalchemy import (
    ForeignKey,
    String,
    UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


if TYPE_CHECKING:
    from .user import User
    from .language import Language


class Setting(Base):
    __tablename__ = "settings"

    id: Mapped[int] = mapped_column(primary_key=True)
    mode: Mapped[str] = mapped_column(String(15), default='dark', nullable=False)
    language_id: Mapped[int] = mapped_column(ForeignKey("languages.id"), nullable=False, default=1)
    type: Mapped[str] = mapped_column(String(15), default="standard")
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, unique=True)

    owner: Mapped['User'] = relationship(back_populates='settings', single_parent=True)

    language: Mapped['Language'] = relationship(back_populates='settings')

__table_args__ = (UniqueConstraint("owner_id"),)
