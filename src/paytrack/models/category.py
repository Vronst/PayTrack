from sqlalchemy import (
    ForeignKey,
    String,
    Boolean,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


# TODO: Study relationships
class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    company_name: Mapped[str | None] = mapped_column(String(80), nullable=True)
    name: Mapped[str] = mapped_column(String(30))
    surname: Mapped[str] = mapped_column(String(30))
    admin: Mapped[bool] = mapped_column(Boolean, default=False)
    email: Mapped[str] = mapped_column(String(50))
    phone: Mapped[str | None] = mapped_column(String(12), nullable=True)
    password: Mapped[str] = mapped_column(String, nullable=False)

    parent_id: Mapped[int | None] = mapped_column(ForeignKey('user.id'), nullable=True)
    subaccounts: Mapped[list['User']] = relationship(
            back_populates='parent_id', cascade='all, delete-orphan'
    )

    part_of: Mapped[int | None] = mapped_column(ForeignKey('user.id'), nullable=True)
    included: Mapped[list["User"]] = relationship(
            back_populates='part_of', cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return \
        f"User(id={self.id!r},admin={self.admin!r},"\
        f" name={self.name!r}, surname={self.surname!r}, email={self.email!r},"\
        f"phone={self.phone!r}, password=****, len(included)={len(self.included) if self.included else 'N/A'}"
    
