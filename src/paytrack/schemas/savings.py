from pydantic import Field

from ..constants.savings import MIN_BUDGET
from ..models import User
from .base import BaseReadSchema, BaseSchema, BaseUpdateSchema


class SavingsSchema(BaseSchema):
    amount: float = Field(ge=MIN_BUDGET)
    currency_id: int
    budget: float | None = Field(ge=MIN_BUDGET, default=None)
    owner_id: int


class SavingsCreateSchema(SavingsSchema):
    pass


class SavingsReadSchema(BaseReadSchema, SavingsSchema):
    included: list[User] = Field(default_factory=list)


class SavingsUpdateSchema(BaseUpdateSchema):
    amount: float | None = None
    currency_id: int | None = None
    budget: float | None = Field(ge=MIN_BUDGET, default=None)
    included: list[User] | None = None
