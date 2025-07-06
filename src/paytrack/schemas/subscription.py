from datetime import datetime
from typing import TYPE_CHECKING, Annotated, Callable
from pydantic import AfterValidator, StringConstraints, Field

from ..validators import ChoiceValidator
from .base import BaseSchema, BaseReadSchema, BaseUpdateSchema
from ..constants.subscription import (
    NAME_LENGTH,
    MIN_AMOUNT,
    PERIOD_CHOICES,
)


if TYPE_CHECKING:
    from ..models import User
    from ..models import SubscriptionShare

validator: Callable = ChoiceValidator(PERIOD_CHOICES).validate


class SubscriptionSchema(BaseSchema):
    name: Annotated[str, StringConstraints(max_length=NAME_LENGTH)]
    amount: float = Field(gt=MIN_AMOUNT)
    currency: int 
    period: Annotated[str, AfterValidator(validator)]
    shared: bool 
    active: bool 
    date: datetime
    owner_id: int


class SubscriptionCreateSchema(SubscriptionSchema):
    pass


class SubscriptionReadSchema(BaseReadSchema, SubscriptionSchema):
    included: list['User'] = Field(default_factory=list)
    subscription_share: list['SubscriptionShare'] = Field(default_factory=list)


class SubscriptionUpdateSchema(BaseUpdateSchema):
    name: Annotated[str | None, StringConstraints(max_length=NAME_LENGTH)] = None
    amount: float | None = Field(gt=MIN_AMOUNT)
    currency: int | None = None
    period: Annotated[str | None, AfterValidator(validator)] = None
    shared: bool | None = None
    active: bool | None = None
    date: datetime | None = None
