"""Base schemas for Subscription."""

from collections.abc import Callable
from datetime import datetime
from typing import Annotated

from pydantic import AfterValidator, Field, StringConstraints

from ..constants.subscription import MIN_AMOUNT, NAME_LENGTH, PERIOD_CHOICES
from ..models import SubscriptionShare, User
from ..validators import ChoiceValidator, DateValidator
from .base import BaseReadSchema, BaseSchema, BaseUpdateSchema

validator: Callable = ChoiceValidator(PERIOD_CHOICES).validate
date_validator: Callable = DateValidator().validate


class SubscriptionSchema(BaseSchema):
    """Base schema for subscription data (excluding updates).

    Attributes:
        name (str): String of length no longer than
        `paytrack.constants.subscription.NAME_LENGTH`.

        amount (float): Float no less than
        `paytrack.constants.subscription.MIN_AMOUNT`.

        currency_id (int): Id of related currency.

        period (str): String that must match one of
        `paytrack.constants.subscription.PERIOD_CHOICES`.

        shared (bool): Shows subscription is shared with someone or not.

        active (bool): Shows subccription is active or not.

        date (datetime): Date from when subscription started. Validated with
        `paytrack.validator.date.DateValidator`.

        owner_id (int): Id of related user.
    """

    # FIXME: date can be 10,
    # FIXME: which creates problems (Field(strict=True)) should help
    name: Annotated[str, StringConstraints(max_length=NAME_LENGTH)]
    amount: float = Field(gt=MIN_AMOUNT)
    currency_id: int
    period: Annotated[str, AfterValidator(validator)]
    shared: bool
    active: bool
    date: Annotated[datetime, AfterValidator(date_validator)]
    owner_id: int


class SubscriptionCreateSchema(SubscriptionSchema):
    """Schema validating data in new subscription entries.

    Same as SubscriptionSchema.
    Created for consinstency.
    """

    pass


class SubscriptionReadSchema(BaseReadSchema, SubscriptionSchema):
    """Schema for reading subscription data from database.

    Inherites after BaseReadSchema, SubscriptionSchema.

    Attributes:
        included (list[User]): List of users that share subscription.
        Default list.

    subscription_share (list[SubscriptionShare]): List of payements
    for this subscription. Default list.
    """

    included: list[User] = Field(default_factory=list)
    subscription_share: list[SubscriptionShare] = Field(default_factory=list)


class SubscriptionUpdateSchema(BaseUpdateSchema):
    """Schema for validating updates to subscription data.

    Attributes:
        name (str | None): String longer than
        `paytrack.constants.subscription.NAME_LENGTH`. Default None.

        amount (float | None): Float greater than
        `paytrack.constants.subscription.MIN_AMOUNT`. Default None.

        currency_id (int | None): Id of related currency. Default None.

        period (str | None): String that must match
        `paytrack.constants.subscription.PERIOD_CHOICES`. Default None.

        shared (bool | None): True if subscription is shared. Default None.

        active (bool | None): True if subscription is active. Default None.

        date (datetime | None): When subscription started. Default None.
        Validated with `paytrack.constants.validator.date.DateValidator`.
    """

    name: Annotated[str | None, StringConstraints(max_length=NAME_LENGTH)] = (
        None
    )
    amount: float | None = Field(gt=MIN_AMOUNT)
    currency_id: int | None = None
    period: Annotated[str | None, AfterValidator(validator)] = None
    shared: bool | None = None
    active: bool | None = None
    date: Annotated[datetime | None, AfterValidator(date_validator)] = None
