from typing import Annotated 
from pydantic import BaseModel, ConfigDict, StringConstraints 

from ..constants.language import CODE_LENGTH, NAME_LENGTH
from .base import BaseReadSchema, BaseSchema


class LanguageSchema(BaseSchema):
    language_code: Annotated[str, StringConstraints(max_length=CODE_LENGTH)]
    language_name: Annotated[str, StringConstraints(max_length=NAME_LENGTH)]


class LanguageCreateSchema(LanguageSchema):
    pass


class LanguageReadSchema(BaseReadSchema, LanguageSchema):
    pass
