from typing import TYPE_CHECKING
from pydantic import Field

from ..constants.savings import MIN_BUDGET
from .base import BaseReadSchema, BaseSchema, BaseUpdateSchema


if TYPE_CHECKING:
    from ..models import User


class SavingsSchema(BaseSchema):
    amount: float = Field(ge=MIN_BUDGET)
    currency_id: int 
    budget: float | None = Field(ge=MIN_BUDGET, default=None)
    owner_id: int


class SavingsCreateSchema(SavingsSchema):
    pass


class SavingsReadSchema(BaseReadSchema, SavingsSchema):
    included: list['User'] = Field(default_factory=list)


class SavingsUpdateSchema(BaseUpdateSchema):
    amount: float | None = None
    currency_id: int | None 
    budget: float | None = Field(ge=MIN_BUDGET, default=None)
    included: list['User'] | None = None

