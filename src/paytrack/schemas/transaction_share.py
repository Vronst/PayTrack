"""Base schemas for TransactionShare."""

from pydantic import Field

from ..constants.transaction_share import MIN_AMOUNT
from ..schemas.base import BaseReadSchema, BaseSchema, BaseUpdateSchema


class TransactionShareSchema(BaseSchema):
    """Base schema for TransactionShare data (excluding updates).

    Attributes:
        owner_id (int): Related user id.

        amount (float): Float greater than
        `paytrack.constants.transaction_share.MIN_AMOUNT`.

        transaction_id (int): Related transactioin id.
    """

    owner_id: int
    amount: float = Field(gt=MIN_AMOUNT)
    transaction_id: int


class TransactionShareCreateSchema(TransactionShareSchema):
    """Schema validating data in new transaction_share entries.

    Same as TransactionShareSchema.
    Created for consinstency.
    """

    pass


class TransactionShareReadSchema(BaseReadSchema, TransactionShareSchema):
    """Schema for reading subscription data from database.

    Inherites after BaseReadSchema, TransactionShareSchema.
    """

    pass


class TransactionShareUpdateSchema(BaseUpdateSchema):
    """Schema for validating updates to transaction_share data.

    Attributes:
        amount (float | None): Float greater than
        `paytrack.constants.transaction_share.MIN_AMOUNT`.
        Default None.

        transaction_id (int | None): Related transactioin id. Default None.
    """

    amount: float | None = Field(default=None, gt=MIN_AMOUNT)
    transaction_id: int | None = None
