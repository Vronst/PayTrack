"""Base schemas for Translation."""

from typing import Annotated

from pydantic import StringConstraints

from ..constants.translation import WORD_LENGTH
from ..schemas.base import BaseReadSchema, BaseSchema, BaseUpdateSchema


class TranslationSchema(BaseSchema):
    """Base schema for translation data (excluding updates).

    Attributes:
        category_id (int): Related category id.

        language_id (int): Related language id.

        word (str): String that must be shorter than
        `paytrack.constants.translation.WORD_LENGTH`.
    """

    category_id: int
    language_id: int
    word: Annotated[str, StringConstraints(max_length=WORD_LENGTH)]


class TranslationCreateSchema(TranslationSchema):
    """Schema validating data in new translation entries.

    Same as TranslationSchema.
    Created for consinstency.
    """

    pass


class TranslationReadSchema(BaseReadSchema, TranslationSchema):
    """Schema for reading translation data from database.

    Inherites after BaseReadSchema, TranslationSchema.
    """

    pass


class TranslationUpdateSchema(BaseUpdateSchema):
    """Schema for validating updates to translation data.

    Attributes:
        category_id (int | None): Related category id. Default None.

        language_id (int | None): Related language id. Default None.

        word (str | None): String that must be shorter than
        `paytrack.constants.translation.WORD_LENGTH`. Default None.
    """

    category_id: int | None = None
    language_id: int | None = None
    word: Annotated[str | None, StringConstraints(max_length=WORD_LENGTH)] = (
        None
    )
