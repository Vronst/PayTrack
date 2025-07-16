from datetime import datetime
from typing import Annotated, Callable

from pydantic import AfterValidator, Field, model_validator

from ..constants.transaction import MIN_AMOUNT, TYPE_CHOICE
from ..schemas.base import BaseReadSchema, BaseSchema, BaseUpdateSchema
from ..validators.choice import ChoiceValidator
from ..validators.schema_validators import validate_receiver

validator: Callable = ChoiceValidator(TYPE_CHOICE).validate


class TransactionSchema(BaseSchema):
    date: datetime
    done: bool
    owner_id: int
    category_id: int
    receiver_id: int | None
    type: Annotated[str, AfterValidator(validator)]
    amount: float = Field(gt=MIN_AMOUNT)
    currency_id: int
    receiver_name: str | None = None

    @model_validator(mode="after")
    def _validate_receiver(self) -> "TransactionSchema":
        validate_receiver(self.receiver_name, self.receiver_id)
        return self


class TransactionCreateSchema(TransactionSchema):
    pass


class TransactionReadSchema(BaseReadSchema, TransactionSchema):
    pass


class TransactionUpdateSchema(BaseUpdateSchema):
    date: datetime | None = None
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
