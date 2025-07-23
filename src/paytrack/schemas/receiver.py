"""Base schemas for Receiver."""

from typing import Annotated

from pydantic import StringConstraints

from ..constants.receiver import NAME_LENGTH
from ..models import User
from .base import BaseReadSchema, BaseSchema, BaseUpdateSchema


class ReceiverSchema(BaseSchema):
    """Base schema for receiver data (excluding updates).

    Attributes:
        owner_id (int): Id of related user.
    name (str): Name of receiver.
    """

    owner_id: int
    name: Annotated[str, StringConstraints(max_length=NAME_LENGTH)]


class ReceiverCreateSchema(ReceiverSchema):
    """Schema for validating new receiver entries.

    Inherites after ReceiverSchema.
    """

    pass


class ReceiverReadSchema(BaseReadSchema, ReceiverSchema):
    """Schema for reading receiver data from the database.

    Inherites after BaseReadSchema, ReceiverSchema.
    """

    included: list[User]


class ReceiverUpdateSchema(BaseUpdateSchema):
    """Schema for validating updates to receiver data.

    Attributes:
        name (str | None): Name of receiver. Default None.

    included (list[User] | None): List of users that can see this receiver.
        Default None.
    """

    name: Annotated[str | None, StringConstraints(max_length=NAME_LENGTH)] = (
        None
    )
    included: list[User] | None = None
