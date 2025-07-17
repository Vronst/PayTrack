from copy import deepcopy  # noqa: D100
from datetime import datetime

import pytest
from pydantic import ValidationError

from paytrack.schemas import (
    LanguageCreateSchema,
    LanguageReadSchema,
    LanguageUpdateSchema,
)

from .conftest import skip_test

create_param: list[dict] = [{"language_code": "PL", "language_name": "Polski"}]

read_param = deepcopy(create_param)
read_param[0]["id"] = 1

update_param = deepcopy(create_param)

missing_fields = [
    "language_name",
    "language_code",
    "id",
]

invalid = [
    ("id", "id"),
    ("language_code", 1),
    ("language_name", 2),
]


@pytest.mark.parametrize("value", create_param)
class TestLangaugeCreate:  # noqa: D101
    class TestValid:  # noqa: D106
        def test_create(self, value):  # noqa: D102
            LanguageCreateSchema(**value)

    class TestInvalid:  # noqa: D106
        @pytest.mark.parametrize(
            "field",
            missing_fields,
            ids=lambda f: f"LanguageCreate_missing_{f}",
        )
        def test_create_missing_field(self, value, field):  # noqa: D102
            skip_test(field, ["id"])
            data = deepcopy(value)
            data.pop(field)

            with pytest.raises(ValidationError):
                LanguageCreateSchema(**data)

        @pytest.mark.parametrize(
            "field, invalid_data",
            invalid,
            ids=lambda f: f"LanguageCreate_invalid_{f}",
        )
        def test_create_invalid_data(self, value, field, invalid_data):  # noqa: D102
            skip_test(field, ["id"])
            data = deepcopy(value)
            data[field] = invalid_data

            with pytest.raises(ValidationError):
                LanguageCreateSchema(**data)


@pytest.mark.parametrize("value", read_param)
class TestLangaugeRead:  # noqa: D101
    class TestValid:  # noqa: D106
        def test_read(self, value):  # noqa: D102
            LanguageReadSchema(**value)

    class TestInvalid:  # noqa: D106
        @pytest.mark.parametrize(
            "field", missing_fields, ids=lambda f: f"LanguageRead_missing_{f}"
        )
        def test_read_missing_field(self, value, field):  # noqa: D102
            data = deepcopy(value)
            data.pop(field)

            with pytest.raises(ValidationError):
                LanguageReadSchema(**data)

        @pytest.mark.parametrize(
            "field, invalid_data",
            invalid,
            ids=lambda f: f"LanguageRead_invalid_{f}",
        )
        def test_read_invalid_data(self, value, field, invalid_data):  # noqa: D102
            data = deepcopy(value)
            data[field] = invalid_data

            with pytest.raises(ValidationError):
                LanguageReadSchema(**data)


@pytest.mark.parametrize("value", update_param)
class TestLangaugeUpdate:  # noqa: D101
    class TestValid:  # noqa: D106
        def test_update(self, value):  # noqa: D102
            result = LanguageUpdateSchema(**value)
            assert (result.updated_at - datetime.now()).total_seconds() < 5

        def test_partial_update(self, value):  # noqa: D102
            data = deepcopy(value)
            data.pop("language_code")

            result = LanguageUpdateSchema(**data)
            assert (result.updated_at - datetime.now()).total_seconds() < 5

    class TestInvalid:  # noqa: D106
        @pytest.mark.parametrize(
            "field, invalid_data",
            invalid,
            ids=lambda f: f"LanguageRead_invalid_{f}",
        )
        def test_update_invalid_data(self, value, field, invalid_data):  # noqa: D102
            skip_test(field, ["id"])
            data = deepcopy(value)
            data[field] = invalid_data

            with pytest.raises(ValidationError):
                LanguageUpdateSchema(**data)
