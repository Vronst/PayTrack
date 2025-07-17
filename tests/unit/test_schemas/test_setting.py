from copy import deepcopy  # noqa: D100
from datetime import datetime

import pytest
from pydantic import ValidationError

from paytrack.constants.setting import MODE_CHOICES
from paytrack.schemas import (
    SettingCreateSchema,
    SettingReadSchema,
    SettingUpdateSchema,
)

from .conftest import skip_test

create_params = [
    {
        "mode": MODE_CHOICES[0],
        "language_id": 1,
        "owner_id": 1,
    }
]

read_params = deepcopy(create_params)
read_params[0]["id"] = 1

update_params = deepcopy(create_params)
update_params[0].pop("owner_id")

invalid_data = [("mode", 10), ("language_id", "str"), ("owner_id", "id")]

missing_fields = [
    "mode",
    "language_id",
    "owner_id",
]


@pytest.mark.parametrize("value", create_params)
class TestSettingCreate:  # noqa: D101
    class TestValid:  # noqa: D106
        def test_create(self, value):  # noqa: D102
            SettingCreateSchema(**value)

    class TestInvalid:  # noqa: D106
        @pytest.mark.parametrize(
            "field,data",
            invalid_data,
            ids=lambda f: f"SettingCreate_invalid_value_{f}",
        )
        def test_create_invalid_data(self, value, data, field):  # noqa: D102
            skip_test(field, ["id"])
            data = deepcopy(value)
            data[field] = data

            with pytest.raises(ValidationError):
                SettingCreateSchema(**data)

        @pytest.mark.parametrize(
            "field", missing_fields, ids=lambda f: f"SettingCreate_missing_{f}"
        )
        def test_create_missing(self, value, field):  # noqa: D102
            data = deepcopy(value)
            data.pop(field)

            with pytest.raises(ValidationError):
                SettingCreateSchema(**data)


@pytest.mark.parametrize("value", read_params)
class TestSettingRead:  # noqa: D101
    class TestValid:  # noqa: D106
        def test_read(self, value):  # noqa: D102
            SettingReadSchema(**value)

    class TestInvalid:  # noqa: D106
        @pytest.mark.parametrize(
            "field,data",
            invalid_data,
            ids=lambda f: f"SettingRead_invalid_value_{f}",
        )
        def test_create_invalid_data(self, value, data, field):  # noqa: D102
            data = deepcopy(value)
            data[field] = data

            with pytest.raises(ValidationError):
                SettingReadSchema(**data)

        @pytest.mark.parametrize(
            "field", missing_fields, ids=lambda f: f"SettingRead_missing_{f}"
        )
        def test_create_missing(self, value, field):  # noqa: D102
            data = deepcopy(value)
            data.pop(field)

            with pytest.raises(ValidationError):
                SettingReadSchema(**data)


@pytest.mark.parametrize("value", update_params)
class TestSettingUpdate:  # noqa: D101
    class TestValid:  # noqa: D106
        def test_update(self, value):  # noqa: D102
            result = SettingUpdateSchema(**value)
            assert (result.updated_at - datetime.now()).total_seconds() < 5

        def test_partial_update(self, value):  # noqa: D102
            data = deepcopy(value)
            data.pop("language_id")

            result = SettingUpdateSchema(**data)
            assert (result.updated_at - datetime.now()).total_seconds() < 5

    class TestInvalid:  # noqa: D106
        def test_update_invalid_mode(self, value):  # noqa: D102
            data = deepcopy(value)
            data["mode"] = "invalid mode"

            with pytest.raises(ValidationError):
                SettingUpdateSchema(**data)

        def test_update_language_str(self, value):  # noqa: D102
            data = deepcopy(value)
            data["language_id"] = "str"

            with pytest.raises(ValidationError):
                SettingUpdateSchema(**data)
