from typing import Annotated
from pydantic import StringConstraints, Field

from ..constants.category import NAME_LENGTH
from .base import BaseSchema, BaseReadSchema


class CategorySchema(BaseSchema):
    root_category: int | None = None
    name: Annotated[str | None, StringConstraints(max_length=NAME_LENGTH)] = None


class CategoryCreateSchema(CategorySchema):
    pass


class CategoryReadSchema(BaseReadSchema, CategorySchema):
    subcategories: list['CategoryReadSchema'] = Field(default_factory=list)
    root: 'CategoryReadSchema | None ' = None


CategoryReadSchema.model_rebuild()
