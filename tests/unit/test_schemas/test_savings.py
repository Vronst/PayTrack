from copy import deepcopy  # noqa: D100

import pytest
from pydantic import ValidationError

from paytrack.schemas import (
    SavingsCreateSchema,
    SavingsReadSchema,
    SavingsUpdateSchema,
)
from paytrack.services.date import utc_now

from .conftest import skip_test

create_param = [
    {
        "amount": 11.5,
        "currency_id": 1,
        "owner_id": 1,
    }
]

read_param = deepcopy(create_param)
read_param[0]["id"] = 1
read_param[0]["included"] = []

update_param = deepcopy(create_param)

missing_fields = [
    "id",
    "owner_id",
    "currency_id",
    "amount",
    "included",
]

invalid_values = [
    ("id", "id"),
    ("amount", "amount"),
    ("currency_id", "currency_id"),
    ("owner_id", "owner_id"),
    ("budget", "budget"),
]


@pytest.mark.parametrize("value", create_param)
class TestSavingsCreate:  # noqa: D101
    class TestValid:  # noqa: D106
        def test_create(self, value):  # noqa: D102
            SavingsCreateSchema(**value)

        def test_create_with_budget(self, value):  # noqa: D102
            data = deepcopy(value)
            data["budget"] = 12.5

            SavingsCreateSchema(**data)

    class TestInvalid:  # noqa: D106
        @pytest.mark.parametrize(
            "field",
            missing_fields,
            ids=lambda f: f"SavingsCreate_missing_{f}",
        )
        def test_create_missing_field(self, value, field):  # noqa: D102
            skip_test(field, ["included", "id"])
            data = deepcopy(value)
            data.pop(field)

            with pytest.raises(ValidationError):
                SavingsCreateSchema(**data)

        @pytest.mark.parametrize(
            "field, invalid_value",
            invalid_values,
            ids=lambda f: f"SavingsCreate_invalid_value_{f}",
        )
        def test_invalid_values(self, value, field, invalid_value):  # noqa: D102
            skip_test(field, ["id", "included"])
            data = deepcopy(value)
            data[field] = invalid_value


@pytest.mark.parametrize("value", read_param)
class TestSavingsRead:  # noqa: D101
    class TestValid:  # noqa: D106
        def test_read(self, value):  # noqa: D102
            SavingsReadSchema(**value)

    class TestInvalid:  # noqa: D106
        @pytest.mark.parametrize(
            "field",
            missing_fields,
            ids=lambda f: f"SavingsRead_missing_{f}",
        )
        def test_missing_field(self, value, field):  # noqa: D102
            skip_test(field, ["included"])
            data = deepcopy(value)
            data.pop(field)

            with pytest.raises(ValidationError):
                SavingsReadSchema(**data)

        @pytest.mark.parametrize(
            "field, invalid_value",
            invalid_values,
            ids=lambda f: f"SavingsRead_invalid_value_{f}",
        )
        def test_invalid_values(self, value, field, invalid_value):  # noqa: D102
            data = deepcopy(value)
            data[field] = invalid_value

            with pytest.raises(ValidationError):
                SavingsReadSchema(**data)


@pytest.mark.parametrize("value", update_param)
class TestSavingsUpdate:  # noqa: D101
    class TestValid:  # noqa: D106
        def test_update(self, value):  # noqa: D102
            data = deepcopy(value)
            data["budget"] = 15.5

            result = SavingsUpdateSchema(**data)
            assert (result.updated_at - utc_now()).total_seconds() < 5

        def test_partial_update(self, value):  # noqa: D102
            result = SavingsUpdateSchema(**value)
            assert (result.updated_at - utc_now()).total_seconds() < 5

    class TestInvalid:  # noqa: D106
        @pytest.mark.parametrize(
            "field, invalid_value",
            invalid_values,
            ids=lambda f: f"SavingsUpdate_invalid_value_{f}",
        )
        def test_invalid_values(self, value, field, invalid_value):  # noqa: D102
            skip_test(field, ["id", "owner_id"])
            data = deepcopy(value)
            data[field] = invalid_value

            with pytest.raises(ValidationError):
                SavingsUpdateSchema(**data)
