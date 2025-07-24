"""Base schemas for subscription share."""

from pydantic import Field

from ..constants.subscription_share import MIN_AMOUNT
from ..schemas.base import BaseReadSchema, BaseSchema, BaseUpdateSchema


class SubscriptionShareSchema(BaseSchema):
    """Base for other subscription_share schemas (excluding updates).

    Attributes:
        amount (float): Float greater than
        `paytrack.constants.subscription_share.MIN_AMOUNT`.

        owner_id (int): Id of related user.

        subscription_id (int): Id of related subscription.
    """

    amount: float = Field(gt=MIN_AMOUNT)
    owner_id: int
    subscription_id: int


class SubscriptionShareCreateSchema(SubscriptionShareSchema):
    """Schema for validating new subscription_share entries.

    Created for consinstency.
    Inherites after SubscriptionShareSchema.
    """

    pass


class SubscriptionShareReadSchema(BaseReadSchema, SubscriptionShareSchema):
    """Schema for reading data from database.

    Inherites after BaseReadSchema, SubscriptionShareSchema.
    """

    pass


class SubscriptionShareUpdateSchema(BaseUpdateSchema):
    """Schema for validating updates to subscription_share data.

    Attributes:
    amount (float | None): Float greater than
    `paytrack.constants.subscription_share.MIN_AMOUNT`. Default None

    subscription_id (int | None): Id of related subscription. Default None.
    """

    amount: float | None = Field(gt=MIN_AMOUNT, default=None)
    subscription_id: int | None = None
