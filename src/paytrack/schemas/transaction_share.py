from pydantic import Field
from ..schemas.base import BaseSchema, BaseUpdateSchema, BaseReadSchema
from ..constants.transaction_share import MIN_AMOUNT


class TransactionShareSchema(BaseSchema):
    owner_id: int 
    amount: float = Field(gt=MIN_AMOUNT)
    transaction_id: int


class TransactionShareCreateSchema(TransactionShareSchema):
    pass


class TransactionShareReadSchema(BaseReadSchema, TransactionShareSchema):
    pass


class TransactionShareUpdateSchema(BaseUpdateSchema):
    amount: float | None = Field(default=None, gt=MIN_AMOUNT)
    transaction_id: int | None = None
