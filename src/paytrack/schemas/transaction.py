from datetime import datetime
from typing import Annotated, Callable
from pydantic import AfterValidator, Field

from ..validators.choice import ChoiceValidator
from ..schemas.base import BaseReadSchema, BaseSchema, BaseUpdateSchema
from ..constants.transaction import MIN_AMOUNT, TYPE_CHOICE


validator: Callable = ChoiceValidator(TYPE_CHOICE)


class TransactionSchema(BaseSchema):
    date: datetime
    done: bool 
    owner_id: int
    category_id: int 
    receiver_id: int | None 
    type: Annotated[str, AfterValidator(validator)]
    amount: float = Field(gt=MIN_AMOUNT)
    currency_id: int 
    receiver_name: str


class TransactionCreateSchema(TransactionSchema):
    pass 


class TransactionReadSchema(BaseReadSchema, TransactionSchema):
    pass


class TransactionUpdateSchema(BaseUpdateSchema):
    date: datetime | None = None 
    done: bool | None = None
    category_id: int | None = None
    receiver_id: int | None = None
    type: Annotated[str | None, AfterValidator(validator)] = None
    amount: float | None = Field(gt=MIN_AMOUNT, default=None)
    currency_id: int | None = None 
    receiver_name: str | None = None

