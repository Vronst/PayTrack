from typing import Annotated, Callable

from pydantic import AfterValidator

from ..constants.setting import MODE_CHOICES
from ..validators import ChoiceValidator
from .base import BaseReadSchema, BaseSchema, BaseUpdateSchema

validator: Callable = ChoiceValidator(MODE_CHOICES).validate


class SettingSchema(BaseSchema):
    mode: Annotated[str, AfterValidator(validator)]
    language_id: int
    owner_id: int


class SettingCreateSchema(SettingSchema):
    pass


class SettingReadSchema(BaseReadSchema, SettingSchema):
    pass


class SettingUpdateSchema(BaseUpdateSchema):
    mode: Annotated[str, AfterValidator(validator)] | None = None
    language_id: int | None = None
