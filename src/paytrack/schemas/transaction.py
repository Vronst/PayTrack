from ..schemas.base import BaseReadSchema, BaseSchema, BaseUpdateSchema


class TransactionSchema(BaseSchema):
    ...


class TransactionCreateSchema(TransactionSchema):
    pass 


class TransactionReadSchema(BaseReadSchema, TransactionSchema):
    ...


class TransactionUpdateSchema(BaseUpdateSchema):
    ...
