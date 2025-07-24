"""Base schema for Setting."""

from collections.abc import Callable
from typing import Annotated

from pydantic import AfterValidator

from ..constants.setting import MODE_CHOICES
from ..validators import ChoiceValidator
from .base import BaseReadSchema, BaseSchema, BaseUpdateSchema

validator: Callable = ChoiceValidator(MODE_CHOICES).validate


class SettingSchema(BaseSchema):
    """Base schema for setting data (excluding updates).

    Attributes:
    mode (str): String that must match
    `paytrack.constants.setting.MODE_CHOICES`.

    language_id (int): Id of related language.

    owner_id (int): Id of related user.
    """

    mode: Annotated[str, AfterValidator(validator)]
    language_id: int
    owner_id: int


class SettingCreateSchema(SettingSchema):
    """Schema for validating new setting entries.

    Inherites after SettingSchema.
    Created for consinstency.
    """

    pass


class SettingReadSchema(BaseReadSchema, SettingSchema):
    """Schema for reading setting data from the database.

    Inherites after BaseReadSchema, SettingSchema.
    """

    pass


class SettingUpdateSchema(BaseUpdateSchema):
    """Schema for validating updates to setting data.

    Attributes:
        mode (str | None): String that must match one of choices from
        `paytrack.constants.setting.MODE_CHOICES`. Default None.

        langauge_id (int | None): Id of related langague. Default None.
    """

    mode: Annotated[str, AfterValidator(validator)] | None = None
    language_id: int | None = None
