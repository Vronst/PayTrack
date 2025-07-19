"""Base classes for CategorySchema."""

from typing import Annotated

from pydantic import Field, StringConstraints, model_validator

from ..constants.category import NAME_LENGTH
from ..models import Category
from ..validators.schema_validators import validate_name_if_custom
from .base import BaseReadSchema, BaseSchema, BaseUpdateSchema


class CategorySchema(BaseSchema):
    """Root of other base classes.

    Contains shared fields and inherits from BaseSchema.

    Params:
        root_category (int | None): default None.
        name (str | None): validated with StringConstraints, defualt None.
    """

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
    """Same as CategorySchema.

    Created for consinstency.
    """

    pass


class CategoryReadSchema(BaseReadSchema, CategorySchema):
    """Extends Base schemas for Category with subcategories.

    Params:
        subcategories (list[Category]): made strict,
        so no conversion will happen.
    """

    subcategories: Annotated[list[Category], Field(strict=True)]


class CategoryUpdateSchema(BaseUpdateSchema):
    """Base for Category - update.

    Params:
        root_category (int | None): default None.
        name (str | None): default None.
    """

    root_category: int | None = None
    name: str | None = None


CategoryReadSchema.model_rebuild()
