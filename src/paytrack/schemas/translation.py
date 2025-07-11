from typing import Annotated

from pydantic import StringConstraints
from ..schemas.base import BaseSchema, BaseUpdateSchema, BaseReadSchema
from ..constants.translation import WORD_LENGTH


class TranslationSchema(BaseSchema):
    category_id: int 
    language_id: int 
    word: Annotated[str, StringConstraints(max_length=WORD_LENGTH)]


class TranslationCreateSchema(TranslationSchema):
    pass


class TranslationReadSchema(BaseReadSchema, TranslationSchema):
    pass


class TranslationUpdateSchema(BaseUpdateSchema):
    category_id: int | None = None
    language_id: int | None = None
    word: Annotated[str | None, StringConstraints(max_length=WORD_LENGTH)] = None
