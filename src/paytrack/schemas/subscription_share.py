from pydantic import Field

from ..constants.subscription_share import MIN_AMOUNT
from ..schemas.base import BaseReadSchema, BaseSchema, BaseUpdateSchema


class SubscriptionShareSchema(BaseSchema):
    amount: float = Field(gt=MIN_AMOUNT)
    owner_id: int
    subscription_id: int


class SubscriptionShareCreateSchema(SubscriptionShareSchema):
    pass


class SubscriptionShareReadSchema(BaseReadSchema, SubscriptionShareSchema):
    pass


class SubscriptionShareUpdateSchema(BaseUpdateSchema):
    amount: float | None = Field(gt=MIN_AMOUNT, default=None)
    subscription_id: int | None = None
