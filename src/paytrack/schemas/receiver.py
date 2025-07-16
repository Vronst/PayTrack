from typing import Annotated

from pydantic import StringConstraints

from ..constants.receiver import NAME_LENGTH
from ..models import User
from .base import BaseReadSchema, BaseSchema, BaseUpdateSchema


class ReceiverSchema(BaseSchema):
    owner_id: int
    name: Annotated[str, StringConstraints(max_length=NAME_LENGTH)]


class ReceiverCreateSchema(ReceiverSchema):
    pass


class ReceiverReadSchema(BaseReadSchema, ReceiverSchema):
    included: list[User]


class ReceiverUpdateSchema(BaseUpdateSchema):
    name: Annotated[str | None, StringConstraints(max_length=NAME_LENGTH)] = (
        None
    )
    included: list[User] | None = None
