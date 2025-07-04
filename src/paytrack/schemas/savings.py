from pydantic import Field

from ..constants.savings import MIN_BUDGET
from .base import BaseReadSchema, BaseSchema


class SavingsSchema(BaseSchema):
    # TODO: finish rest of the classes
    amount: float = Field(ge=MIN_BUDGET)
    currency_id: int 
    budget: float | None = Field(ge=MIN_BUDGET, default=None)
    owner_id: int


class SavingsCreateSchema(SavingsSchema):
    pass


class SavingsReadSchema(BaseReadSchema, SavingsSchema):
    included: list['SavingsReadSchema'] = Field(default_factory=list)

