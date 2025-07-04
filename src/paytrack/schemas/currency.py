from typing import Annotated
from pydantic import StringConstraints 

from ..constants.currency import NAME_LENGTH, CODE_LENGTH
from .base import BaseReadSchema, BaseSchema


class CurrencySchema(BaseSchema):
    code: Annotated[str, StringConstraints(max_length=CODE_LENGTH)]
    name: Annotated[str, StringConstraints(max_length=NAME_LENGTH)]
    value: float


class CurrencyCreateSchema(CurrencySchema):
    pass
    

class CurrencyReadSchema(BaseReadSchema, CurrencySchema):
    pass
