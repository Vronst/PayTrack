from typing import Annotated 
from pydantic import StringConstraints 

from ..constants.language import CODE_LENGTH, NAME_LENGTH
from .base import BaseReadSchema, BaseSchema, BaseUpdateSchema


class LanguageSchema(BaseSchema):
    language_code: Annotated[str, StringConstraints(max_length=CODE_LENGTH)]
    language_name: Annotated[str, StringConstraints(max_length=NAME_LENGTH)]


class LanguageCreateSchema(LanguageSchema):
    pass


class LanguageReadSchema(BaseReadSchema, LanguageSchema):
    pass


class LanguageUpdateSchema(BaseUpdateSchema):
    language_code: Annotated[str | None, StringConstraints(max_length=CODE_LENGTH)] = None
    language_name: Annotated[str | None, StringConstraints(max_length=NAME_LENGTH)] = None
