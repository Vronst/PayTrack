from typing import TYPE_CHECKING
from pydantic import BaseModel, ConfigDict


if TYPE_CHECKING:
    from datetime import datetime


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, revalidate_instances='always')

    id: int 
    created_at: 'datetime'
    updated_at: 'datetime | None' 
    deleted_at: 'datetime | None' 


class BaseReadSchema(BaseSchema):
    id: int
