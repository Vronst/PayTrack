from typing import Annotated
from pydantic import StringConstraints, Field, model_validator

from ..constants.category import NAME_LENGTH
from .base import BaseSchema, BaseReadSchema, BaseUpdateSchema
from ..models import Category


class CategorySchema(BaseSchema):
    root_category: int | None = None
    name: Annotated[str | None, StringConstraints(max_length=NAME_LENGTH)] = None
    custom: bool = False

    @model_validator(mode='after')
    def validate_name_if_custom(self) -> 'CategorySchema':
        if self.custom and not self.name:
            raise ValueError('Name for custom categories must be provided')
        elif not self.custom and self.name:
            raise ValueError('Name for non custom categories cannot be edited')
        else:
            return self


class CategoryCreateSchema(CategorySchema):
    pass


class CategoryReadSchema(BaseReadSchema, CategorySchema):
    subcategories: Annotated[list[Category], Field(strict=True)] 


class CategoryUpdateSchema(BaseUpdateSchema):
    root_category: int | None = None
    name: str | None = None



CategoryReadSchema.model_rebuild()
