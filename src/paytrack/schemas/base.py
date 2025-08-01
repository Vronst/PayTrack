"""Base for all schemas.

Contains base classes for:
- update,
- read,
- create
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from ..services.date import utc_now

CONFIG: ConfigDict = ConfigDict(
    from_attributes=True,
    revalidate_instances="always",
    arbitrary_types_allowed=True,
)


class BaseSchema(BaseModel):
    """Default schema with shared CONFIG.

    Attributes:
        model_config (ConfigDict): shared config,
        set with module variable CONFIG.
    """

    model_config = CONFIG


class BaseReadSchema(BaseSchema):
    """BaseSchema extended with id (int) param."""

    id: int


class BaseUpdateSchema(BaseModel):
    """Base class for updateing schemas.

    Attributes:
        model_config (ConfigDict): shared config,
    set with module variable CONFIG.
        id (int | None): default None.
        updated_at (datetime): default datetime.now(UTC).
        deleted_at (datetime | None): default None.
    """

    model_config = CONFIG

    id: int | None = None
    updated_at: "datetime" = Field(default_factory=utc_now)
    delete_at: "datetime | None" = None
