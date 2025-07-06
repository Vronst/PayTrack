from typing import TYPE_CHECKING, Annotated
from pydantic import StringConstraints 

from ..constants.receiver import NAME_LENGTH
from .base import BaseReadSchema, BaseSchema, BaseUpdateSchema


if TYPE_CHECKING:
    from ..models import Receiver
    from .user import UserReadSchema


class ReceiverSchema(BaseSchema):
    owner_id: int 
    name: Annotated[str, StringConstraints(max_length=NAME_LENGTH)]
    

class ReceiverCreateSchema(ReceiverSchema):
    pass


class ReceiverReadSchema(BaseReadSchema, ReceiverSchema):
    included: list['UserReadSchema'] | None = None


class ReceiverUpdateSchema(BaseUpdateSchema):
    name: Annotated[str | None, StringConstraints(max_length=NAME_LENGTH)] = None
    included: list['Receiver'] | None = None


ReceiverReadSchema.model_rebuild()
