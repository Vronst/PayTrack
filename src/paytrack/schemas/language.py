"""Base schemas for Language."""

from typing import Annotated

from pydantic import StringConstraints

from ..constants.language import CODE_LENGTH, NAME_LENGTH
from .base import BaseReadSchema, BaseSchema, BaseUpdateSchema


class LanguageSchema(BaseSchema):
    """Base schema for language data (excluding updates).

    Attributes:
        language_code (str): String no longer than
        `paytrack.constants.language.CODE_LENGTH`.

        language_name (str): String no longer than
        `paytrack.constants.language.NAME_LENGTH`.
    """

    language_code: Annotated[str, StringConstraints(max_length=CODE_LENGTH)]
    language_name: Annotated[str, StringConstraints(max_length=NAME_LENGTH)]


class LanguageCreateSchema(LanguageSchema):
    """Schema for validating new language entries.

    Inherites after base LanguageSchema.
    """

    pass


class LanguageReadSchema(BaseReadSchema, LanguageSchema):
    """Schema for reading currency data from the database.

    Inherites after BaseReadSchema, LanguageSchema.
    """

    pass


class LanguageUpdateSchema(BaseUpdateSchema):
    """Schema for validating updates to language data.

    Attributes:
    language_code (str | None): String no longer than
    `paytrack.constants.language.CODE_LENGTH`. Default None.

    language_name (str | None): String no longer than
    `paytrack.constants.language.NAME_LENGTH`. Default None.
    """

    language_code: Annotated[
        str | None, StringConstraints(max_length=CODE_LENGTH)
    ] = None
    language_name: Annotated[
        str | None, StringConstraints(max_length=NAME_LENGTH)
    ] = None
