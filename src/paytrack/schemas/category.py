from typing import TYPE_CHECKING, Annotated
from pydantic import StringConstraints, Field

from ..constants.category import NAME_LENGTH
from .base import BaseSchema, BaseReadSchema, BaseUpdateSchema


if TYPE_CHECKING:
    from ..models import Transaction
    from ..models import Category


class CategorySchema(BaseSchema):
    root_category: int | None = None
    name: Annotated[str | None, StringConstraints(max_length=NAME_LENGTH)] = None


class CategoryCreateSchema(CategorySchema):
    pass


class CategoryReadSchema(BaseReadSchema, CategorySchema):
    subcategories: list['CategoryReadSchema'] = Field(default_factory=list)
    root: 'CategoryReadSchema | None ' = None


class CategoryUpdateSchema(BaseUpdateSchema):
    root: 'Category | None' = None



CategoryReadSchema.model_rebuild()
