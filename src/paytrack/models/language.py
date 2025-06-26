# from typing import TYPE_CHECKING
from sqlalchemy import (
    String,
)
from sqlalchemy.orm import Mapped, mapped_column  # , relationship
from .base import Base


# if TYPE_CHECKING:
#     from .setting import Setting


class Language(Base):
    __tablename__ = "languages"

    id: Mapped[int] = mapped_column(primary_key=True)
    language_code: Mapped[str] = mapped_column(String(2), unique=True, nullable=False)
    language_name: Mapped[str] = mapped_column(String(15), unique=True, nullable=False)
    
    # settings: Mapped[list['Setting']] = relationship(back_populates='language')
