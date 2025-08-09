"""Base schemas for User."""

from collections.abc import Callable
from typing import Annotated

from pydantic import AfterValidator, StringConstraints

from ..constants.user import EMAIL_LENGTH, NAME_LENGTH, PIN_LENGTH
from ..models import User
from ..validators import EmailValidator, PhoneValidator, PinValidator
from .base import BaseReadSchema, BaseSchema, BaseUpdateSchema

pin_validator: Callable = PinValidator(PIN_LENGTH).validate
phone_validator: Callable = PhoneValidator().validate
email_validator: Callable = EmailValidator().validate


class UserSchema(BaseSchema):
    """Base schema for user data (excluding updates).

    Attributes:
        name (str): User name.

        surname (str | None): User surname,
        only valid if company is set to False.
        Default None.

        email (str): String verified with `paytrack.validators.EmailValidator`.
        Should be a valid email.

        phone (str | None): String verified with
        `paytrack.validators.PhoneValidator`.
        Should be a valid phone.

        premium (bool): If True, user has premium account.

        parent_id (int | None): Id of parent account. Default None.
    """

    name: Annotated[str, StringConstraints(max_length=NAME_LENGTH)]
    surname: Annotated[
        str | None, StringConstraints(max_length=NAME_LENGTH)
    ] = None
    email: Annotated[
        str,
        AfterValidator(email_validator),
        StringConstraints(max_length=EMAIL_LENGTH),
    ]
    phone: Annotated[str | None, AfterValidator(phone_validator)]
    premium: bool
    parent_id: int | None = None


class UserCreateSchema(UserSchema):
    """Schema validating data in new user entries.

    Attributes:
        password (str): String.
        pin (str): String.
    """

    password: str | None = None
    pin: Annotated[str | None, AfterValidator(pin_validator)] = None


class UserReadSchema(BaseReadSchema, UserSchema):
    """Schema for reading user data from database.

        Inherites after BaseReadSchema, UserSchema.

    Attributes:
            subaccounts (list[User]): List of other accounts,
            which has this account id,
            as parent id.

            included (list[User]): List of users,
            that can see every transaction of this account.
    """

    subaccounts: list[User]
    included: list[User]


class UserUpdateSchema(BaseUpdateSchema):
    """Schema for validating updates to user data.

    Attributes:
        name (str | None): User name. Default None.

        surname (str | None): User surname,
        only valid if company is set to False.
        Default None.

        email (str | None): String verified with
        `paytrack.validators.EmailValidator`.
        Should be a valid email. Default None.

        phone (str | None): String verified with
        `paytrack.validators.PhoneValidator`.
        Should be a valid phone. Default None.

        premium (bool | None): If True, user has premium account.

        password (str | None): password of user. Default None.

        pin (str | None): Default None.

        subaccounts (list[User]): List of subaccounts. Default None.

        included (list[User]): List of user to share account with.
        Default None.
    """

    name: Annotated[str | None, StringConstraints(max_length=NAME_LENGTH)] = (
        None
    )
    surname: Annotated[
        str | None, StringConstraints(max_length=NAME_LENGTH)
    ] = None
    email: Annotated[
        str | None,
        AfterValidator(email_validator),
        StringConstraints(max_length=EMAIL_LENGTH),
    ] = None
    phone: Annotated[str | None, AfterValidator(phone_validator)] = None
    premium: bool | None = None
    parent_id: int | None = None
    password: str | None = None
    pin: Annotated[str | None, AfterValidator(pin_validator)] = None
    subaccounts: list[User] | None = None
    included: list[User] | None = None
