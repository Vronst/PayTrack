"""Base schema for Savings."""

from pydantic import Field

from ..constants.savings import MIN_BUDGET
from ..models import User
from .base import BaseReadSchema, BaseSchema, BaseUpdateSchema


class SavingsSchema(BaseSchema):
    """Base schema for Savings data (excluding updates).

    Attributes:
    amount (float): Float greater than `paytrack.constants.savings.MIN_BUDGET`.

    currency_id (int): Id of currency.

    budget (float | None): Float greater than
    `paytrack.constants.savings.MIN_BUDGET`. Default None.

    owner_id (int): Id of owner.
    """

    amount: float = Field(ge=MIN_BUDGET)
    currency_id: int
    budget: float | None = Field(ge=MIN_BUDGET, default=None)
    owner_id: int


class SavingsCreateSchema(SavingsSchema):
    """Schema for validating new savings entries.

    Inherites after SavingsSchema.
    Created for consinstency.
    """

    pass


class SavingsReadSchema(BaseReadSchema, SavingsSchema):
    """Schema for reading currency data from the database.

    Inherites after BaseReadSchema, SavingsSchema.
    """

    included: list[User] = Field(default_factory=list)


class SavingsUpdateSchema(BaseUpdateSchema):
    """Schema for validating updates to currency data.

    Attributes:
    amount (float | None): Default None.

    currency_id (int | None): Default None.

    budget (float | None): Float greater than `paytrack.constants.savings.MIN_BUDGET`.
    Default None.

    included (list[User] | None): List of user that can see this entry.
    Default None.
    """

    amount: float | None = None
    currency_id: int | None = None
    budget: float | None = Field(ge=MIN_BUDGET, default=None)
    included: list[User] | None = None
