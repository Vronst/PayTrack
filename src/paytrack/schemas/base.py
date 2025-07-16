from datetime import datetime

from pydantic import BaseModel, ConfigDict

CONFIG: ConfigDict = ConfigDict(
    from_attributes=True,
    revalidate_instances="always",
    arbitrary_types_allowed=True,
)


class BaseSchema(BaseModel):
    model_config = CONFIG
    # created_at: 'datetime' = datetime.now()
    # updated_at: 'datetime | None' = None
    # deleted_at: 'datetime | None' = None


class BaseReadSchema(BaseSchema):
    id: int


class BaseUpdateSchema(BaseModel):
    model_config = CONFIG

    id: int | None = None
    updated_at: "datetime" = datetime.now()
    delete_at: "datetime | None" = None
