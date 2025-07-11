from datetime import datetime
from typing import Annotated, Callable
from pydantic import AfterValidator, StringConstraints, Field

from ..validators import ChoiceValidator, DateValidator
from .base import BaseSchema, BaseReadSchema, BaseUpdateSchema
from ..constants.subscription import (
    NAME_LENGTH,
    MIN_AMOUNT,
    PERIOD_CHOICES,
)
from ..models import User
from ..models import SubscriptionShare


validator: Callable = ChoiceValidator(PERIOD_CHOICES).validate
date_validator: Callable = DateValidator().validate


class SubscriptionSchema(BaseSchema):
    # FIXME: date can be 10, which creates problems
    name: Annotated[str, StringConstraints(max_length=NAME_LENGTH)]
    amount: float = Field(gt=MIN_AMOUNT)
    currency_id: int 
    period: Annotated[str, AfterValidator(validator)]
    shared: bool 
    active: bool 
    date: Annotated[datetime, AfterValidator(date_validator)]
    owner_id: int


class SubscriptionCreateSchema(SubscriptionSchema):
    pass


class SubscriptionReadSchema(BaseReadSchema, SubscriptionSchema):
    included: list[User] = Field(default_factory=list)
    subscription_share: list[SubscriptionShare] = Field(default_factory=list)


class SubscriptionUpdateSchema(BaseUpdateSchema):
    name: Annotated[str | None, StringConstraints(max_length=NAME_LENGTH)] = None
    amount: float | None = Field(gt=MIN_AMOUNT)
    currency_id: int | None = None
    period: Annotated[str | None, AfterValidator(validator)] = None
    shared: bool | None = None
    active: bool | None = None
    date: Annotated[datetime | None, AfterValidator(date_validator)] = None

