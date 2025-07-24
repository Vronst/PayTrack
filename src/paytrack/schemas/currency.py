"""Base schemas for Currency."""

from typing import Annotated

from pydantic import StringConstraints

from ..constants.currency import CODE_LENGTH, NAME_LENGTH
from .base import BaseReadSchema, BaseSchema, BaseUpdateSchema


class CurrencySchema(BaseSchema):
    """Base schema for currency data (excluding updates).

    Attributes:
        name (str): String no longer than
        `paytrack.constants.currency.NAME_LENGTH`.

        code (str): String no longer than
        `paytrack.constants.currency.CODE_LENGTH`.

        value (float): Multiplier of this currency against EURO.
    """

    code: Annotated[str, StringConstraints(max_length=CODE_LENGTH)]
    name: Annotated[str, StringConstraints(max_length=NAME_LENGTH)]
    value: float


class CurrencyCreateSchema(CurrencySchema):
    """Schema for validating new currency entries.

    Inherites after base CurrencySchema.
    Created for consinstency.
    """

    pass


class CurrencyReadSchema(BaseReadSchema, CurrencySchema):
    """Schema for reading currency data from the database.

    Inherites after base CurrencySchema and BaseReadSchema.
    """

    pass


class CurrencyUpdateSchema(BaseUpdateSchema):
    """Schema for validating updates to currency data.

    Attributes:
        name (str | None): String no longer than
        `paytrack.constants.currency.NAME_LENGTH`. Default None.

        code (str | None): str no longer than
        `paytrack.constants.currency.CODE_LENGTH`. Default None.

        value (float | None): Multiplier of this currency against EURO.
        Default None.
    """

    code: Annotated[str | None, StringConstraints(max_length=CODE_LENGTH)] = (
        None
    )
    name: Annotated[str | None, StringConstraints(max_length=NAME_LENGTH)] = (
        None
    )
    value: float | None = None
