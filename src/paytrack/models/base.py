from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import (
    mapped_column,
    Mapped,
)


class Base(DeclarativeBase):
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, default=None, nullable=True, onupdate=datetime.now)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, default=None, nullable=True)
