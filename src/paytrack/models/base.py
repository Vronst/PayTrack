"""SQLAlchemy Base for all models."""

from datetime import UTC, datetime

from sqlalchemy import DateTime
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    """Base for all models.

    Required by SQLAlchemy.
    Ships with 3 fields:
    - created_at,
    - updated_at,
    - deleted_at
    """

    __abstract__ = True

    def utc_now(self) -> datetime:
        """Returns datetime.now(UTC)."""
        return datetime.now(UTC)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, nullable=False
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime, default=None, nullable=True, onupdate=utc_now
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime, default=None, nullable=True
    )
