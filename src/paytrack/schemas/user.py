from typing import Annotated, Callable

from pydantic import AfterValidator, StringConstraints

from ..validators import EmailValidator, PhoneValidator, PinValidator
from .base import BaseReadSchema, BaseUpdateSchema, BaseSchema
from ..constants.user import EMAIL_LENGTH, NAME_LENGTH, PIN_LENGTH
from ..models import User


pin_validator: Callable = PinValidator(PIN_LENGTH).validate
phone_validator: Callable = PhoneValidator().validate
email_validator: Callable = EmailValidator().validate


class UserSchema(BaseSchema):
    name: Annotated[str, StringConstraints(max_length=NAME_LENGTH)]
    surname: Annotated[str | None, StringConstraints(max_length=NAME_LENGTH)]
    admin: bool 
    email: Annotated[
    str,
    AfterValidator(email_validator),
    StringConstraints(max_length=EMAIL_LENGTH)
]
    phone: Annotated[str | None, AfterValidator(phone_validator)]
    premium: bool
    parent_id: int | None = None


class UserCreateSchema(UserSchema):
    pass


class UserReadSchema(BaseReadSchema, UserSchema):
    subaccounts: list[User]
    included: list[User]


class UserUpdateSchema(BaseUpdateSchema):
    name: Annotated[str | None, StringConstraints(max_length=NAME_LENGTH)] = None
    surname: Annotated[str | None, StringConstraints(max_length=NAME_LENGTH)] = None
    admin: bool | None = None
    email: Annotated[
    str | None,
    AfterValidator(email_validator),
    StringConstraints(max_length=EMAIL_LENGTH)
    ] = None
    phone: Annotated[str | None, AfterValidator(phone_validator)] = None
    premium: bool | None = None
    parent_id: int | None = None
    password: str | None = None
    pin: Annotated[str | None, AfterValidator(pin_validator)] = None
    subaccounts: list[User] | None = None
    included: list[User] | None = None

