from typing import Annotated
from pydantic import StringConstraints 

from ..constants.receiver import NAME_LENGTH
from .base import BaseReadSchema, BaseSchema


class ReceiverSchema(BaseSchema):
    owner_id: int 
    name: Annotated[str, StringConstraints(max_length=NAME_LENGTH)]
    

class ReceiverCreateSchema(ReceiverSchema):
    pass


class ReceiverReadSchema(BaseReadSchema, ReceiverSchema):
    included: list['ReceiverReadSchema'] | None = None


ReceiverReadSchema.model_rebuild()
