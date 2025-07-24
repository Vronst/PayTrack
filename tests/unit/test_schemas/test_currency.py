from copy import deepcopy  # noqa: D100

import pytest
from pydantic import ValidationError

from paytrack.schemas import (
    CurrencyCreateSchema,
    CurrencyReadSchema,
    CurrencyUpdateSchema,
)
from paytrack.services.date import utc_now

from .conftest import skip_test

create_param = [{"code": "PLN", "name": "Złoty", "value": 12.5}]

read_param = deepcopy(create_param)
read_param[0]["id"] = 1

update_param = deepcopy(create_param)

missing_fields = [
    "code",
    "id",
    "name",
    "value",
]

invalid = [
    ("code", 1),
    ("name", 2),
    ("value", "value"),
    ("id", "id"),
]


@pytest.mark.parametrize("value", create_param)
class TestCurrencyCreate:  # noqa: D101
    class TestValid:  # noqa: D106
        def test_creation(self, value):  # noqa: D102
            CurrencyCreateSchema(**value)

    class TestInvalid:  # noqa: D106
        @pytest.mark.parametrize(
            "field",
            missing_fields,
            ids=lambda f: f"CurrencyCreate_missing_{f}",
        )
        def test_create_missing(self, value, field):  # noqa: D102
            skip_test(field, ["id"])

            data = deepcopy(value)
            data.pop(field)

            with pytest.raises(ValidationError):
                CurrencyCreateSchema(**data)

        @pytest.mark.parametrize(
            "field, invalid_data",
            invalid,
            ids=lambda f: f"CurrencyCreate_invalid_{f}",
        )
        def test_create_invalid_data(self, value, field, invalid_data):  # noqa: D102
            skip_test(field, ["id"])

            data = deepcopy(value)
            data[field] = invalid_data

            with pytest.raises(ValidationError):
                CurrencyCreateSchema(**data)


@pytest.mark.parametrize("value", read_param)
class TestCurrencyRead:  # noqa: D101
    class TestValid:  # noqa: D106
        def test_read(self, value):  # noqa: D102
            CurrencyReadSchema(**value)

    class TestInvalid:  # noqa: D106
        @pytest.mark.parametrize(
            "field", missing_fields, ids=lambda f: f"CurrencyRead_missing_{f}"
        )
        def test_read_missing(self, value, field):  # noqa: D102
            data = deepcopy(value)
            data.pop(field)

            with pytest.raises(ValidationError):
                CurrencyReadSchema(**data)

        @pytest.mark.parametrize(
            "field, invalid_data",
            invalid,
            ids=lambda f: f"CurrencyRead_invalid_{f}",
        )
        def test_read_invalid_data(self, value, field, invalid_data):  # noqa: D102
            data = deepcopy(value)
            data[field] = invalid_data

            with pytest.raises(ValidationError):
                CurrencyReadSchema(**data)


@pytest.mark.parametrize("value", update_param)
class TestCurrencyUpdate:  # noqa: D101
    class TestValid:  # noqa: D106
        def test_update(self, value):  # noqa: D102
            result = CurrencyUpdateSchema(**value)
            assert (result.updated_at - utc_now()).total_seconds() < 5

        @pytest.mark.parametrize(
            "field",
            missing_fields,
            ids=lambda f: f"CurrencyUpdate_missing_{f}",
        )
        def test_partial_update(self, value, field):  # noqa: D102
            skip_test(field, ["id"])
            data = deepcopy(value)
            data.pop(field)

            result = CurrencyUpdateSchema(**data)
            assert (result.updated_at - utc_now()).total_seconds() < 5

    class TestInvalid:  # noqa: D106
        @pytest.mark.parametrize(
            "field, invalid_data",
            invalid,
            ids=lambda f: f"CurrencyUpdate_invalid_{f}",
        )
        def test_update_invalid_data(self, value, field, invalid_data):  # noqa: D102
            skip_test(field, ["id"])
            data = deepcopy(value)
            data[field] = invalid_data

            with pytest.raises(ValidationError):
                CurrencyUpdateSchema(**data)
