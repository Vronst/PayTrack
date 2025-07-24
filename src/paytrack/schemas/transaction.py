"""Base schemas for Transaction."""

from collections.abc import Callable
from datetime import datetime
from typing import Annotated

from pydantic import AfterValidator, Field, model_validator

from ..constants.transaction import MIN_AMOUNT, TYPE_CHOICE
from ..schemas.base import BaseReadSchema, BaseSchema, BaseUpdateSchema
from ..validators import ChoiceValidator, DateValidator
from ..validators.schema_validators import validate_receiver

date_validator: Callable = DateValidator().validate
validator: Callable = ChoiceValidator(TYPE_CHOICE).validate


class TransactionSchema(BaseSchema):
    """Base schema for transaction data (excluding updates).

    Attributes:
        date (datetime): Date of transaction.

        done (bool): True if transaction is already done.

        owner_id (int): Id of related user.

        category_id (int): Id of related category.

        receiver_id (int | None): Id of related receiver. Default None.

        type (str): String that must match
        `paytrack.constants.transaction.TYPE_CHOICE`.

        amount (float): Float greater than
        `paytrack.constants.transaction.MIN_AMOUNT`.

        currency_id (int): Id or related currency.

        receiver_name (str | None): Should not be None,
        only if receiver_id is None.
    """

    date: Annotated[datetime, AfterValidator(date_validator)]
    done: bool
    owner_id: int
    category_id: int
    receiver_id: int | None = None
    type: Annotated[str, AfterValidator(validator)]
    amount: float = Field(gt=MIN_AMOUNT)
    currency_id: int
    receiver_name: str | None

    @model_validator(mode="after")
    def _validate_receiver(self) -> "TransactionSchema":
        validate_receiver(self.receiver_name, self.receiver_id)
        return self


class TransactionCreateSchema(TransactionSchema):
    """Schema validating data in new transaction entries.

    Same as TransactionSchema.
    Created for consinstency.
    """

    pass


class TransactionReadSchema(BaseReadSchema, TransactionSchema):
    """Schema for reading data from database.

    Inherites after BaseReadSchema, TransactionSchema.
    """

    pass


class TransactionUpdateSchema(BaseUpdateSchema):
    """Schema for validating updates to transaction data.

    Attributes:
    date (datetime | None): Date of transaction. Default None.

    done (bool): True if transaction is already done. Default None.

    category_id (int): Id of related category. Default None.

    receiver_id (int | None): Id of related receiver. Default None.

    type (str): String that must match
    `paytrack.constants.transaction.TYPE_CHOICE`. Default None.

    amount (float): Float greater than
    `paytrack.constants.transaction.MIN_AMOUNT`. Default None.

    currency_id (int): Id or related currency. Default None.

    receiver_name (str | None): Should not be None,
    only if receiver_id is None. Default None.
    """

    date: Annotated[datetime | None, AfterValidator(date_validator)] = None
    done: bool | None = None
    category_id: int | None = None
    receiver_id: int | None = None
    type: Annotated[str | None, AfterValidator(validator)] = None
    amount: float | None = Field(gt=MIN_AMOUNT, default=None)
    currency_id: int | None = None
    receiver_name: str | None = None

    @model_validator(mode="after")
    def _validate_receiver(self) -> "TransactionUpdateSchema":
        validate_receiver(self.receiver_name, self.receiver_id)
        return self
