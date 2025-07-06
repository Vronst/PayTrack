from typing import TYPE_CHECKING, Annotated, Callable

from pydantic import AfterValidator, StringConstraints

from ..validators import EmailValidator, PhoneValidator, PinValidator
from .base import BaseReadSchema, BaseUpdateSchema, BaseSchema
from ..constants.user import EMAIL_LENGTH, PHONE_LENGTH, NAME_LENGTH


pin_validator: Callable = PinValidator().validate
phone_validator: Callable = PhoneValidator().validate
email_validator: Callable = EmailValidator().validate

if TYPE_CHECKING:
    from ..models import User


class UserSchema(BaseSchema):
    name: Annotated[str, StringConstraints(max_length=NAME_LENGTH)]
    surname: Annotated[str | None, StringConstraints(max_length=NAME_LENGTH)]
    admin: bool 
    email: Annotated[
    str,
    AfterValidator(email_validator),
    StringConstraints(max_length=EMAIL_LENGTH)
]
    phone: Annotated[str | None, StringConstraints(max_length=PHONE_LENGTH), AfterValidator(phone_validator)]
    premium: bool
    parent_id: int


class UserCreateSchema(UserSchema):
    pass


class UserReadSchema(BaseReadSchema, UserSchema):
    subaccounts: list['User']
    included: list['User']


class UserUpdateSchema(BaseUpdateSchema):
    name: Annotated[str | None, StringConstraints(max_length=NAME_LENGTH)] = None
    surname: Annotated[str | None, StringConstraints(max_length=NAME_LENGTH)] = None
    admin: bool | None = None
    email: Annotated[
    str | None,
    AfterValidator(email_validator),
    StringConstraints(max_length=EMAIL_LENGTH)
]
    phone: Annotated[str | None, StringConstraints(max_length=PHONE_LENGTH), AfterValidator(phone_validator)] = None
    premium: bool | None = None
    parent_id: int | None = None
    password: str | None = None
    pin: Annotated[str | None, AfterValidator(pin_validator)] = None
