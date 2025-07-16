from typing import Annotated

from pydantic import Field, StringConstraints, model_validator

from ..constants.category import NAME_LENGTH
from ..models import Category
from ..validators.schema_validators import validate_name_if_custom
from .base import BaseReadSchema, BaseSchema, BaseUpdateSchema


class CategorySchema(BaseSchema):
    root_category: int | None = None
    name: Annotated[str | None, StringConstraints(max_length=NAME_LENGTH)] = (
        None
    )
    custom: bool = False

    @model_validator(mode="after")
    def _validate_name_if_custom(self) -> "CategorySchema":
        validate_name_if_custom(self.name, self.custom)
        return self


class CategoryCreateSchema(CategorySchema):
    pass


class CategoryReadSchema(BaseReadSchema, CategorySchema):
    subcategories: Annotated[list[Category], Field(strict=True)]


class CategoryUpdateSchema(BaseUpdateSchema):
    root_category: int | None = None
    name: str | None = None


CategoryReadSchema.model_rebuild()
