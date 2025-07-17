from copy import deepcopy  # noqa: D100
from datetime import datetime

import pytest
from pydantic import ValidationError

from paytrack.schemas import (
    ReceiverCreateSchema,
    ReceiverReadSchema,
    ReceiverUpdateSchema,
)

from .conftest import skip_test

create_param = [{"owner_id": 1, "name": "name"}]

read_param = deepcopy(create_param)
read_param[0]["id"] = 1
read_param[0]["included"] = []

update_param = deepcopy(create_param)
update_param[0].pop("owner_id")
update_param[0]["included"] = []

missing_field = ["owner_id", "name", "included"]

invalid = [("owner_id", "owner_id"), ("name", 2), ("included", "included")]


@pytest.mark.parametrize("value", create_param)
class TestReceiverCreate:  # noqa: D101
    class TestValid:  # noqa: D106
        def test_create(self, value):  # noqa: D102
            ReceiverCreateSchema(**value)

    class TestInvalid:  # noqa: D106
        @pytest.mark.parametrize(
            "field",
            missing_field,
            ids=lambda f: f"ReceiverCreate_missing_field_{f}",
        )
        def test_create_missing_field(self, value, field):  # noqa: D102
            skip_test(field, ["included"])
            data = deepcopy(value)
            data.pop(field)

            with pytest.raises(ValidationError):
                ReceiverCreateSchema(**data)

        @pytest.mark.parametrize(
            "field, invalid_data",
            invalid,
            ids=lambda f: f"ReceiverCreate_missing_field_{f}",
        )
        def test_create_invalid_data(self, value, field, invalid_data):  # noqa: D102
            skip_test(field, ["included"])
            data = deepcopy(value)
            data[field] = invalid_data

            with pytest.raises(ValidationError):
                ReceiverCreateSchema(**data)


@pytest.mark.parametrize("value", read_param)
class TestReceiverRead:  # noqa: D101
    class TestValid:  # noqa: D106
        def test_read(self, value):  # noqa: D102
            ReceiverReadSchema(**value)

    class TestInvalid:  # noqa: D106
        @pytest.mark.parametrize(
            "field",
            missing_field,
            ids=lambda f: f"ReceiverRead_missing_field_{f}",
        )
        def test_read_missing_field(self, value, field):  # noqa: D102
            data = deepcopy(value)
            data.pop(field)

            with pytest.raises(ValidationError):
                ReceiverReadSchema(**data)

        @pytest.mark.parametrize(
            "field, invalid_data",
            invalid,
            ids=lambda f: f"ReceiverRead_invalid_{f}",
        )
        def test_read_invalid_data(self, value, field, invalid_data):  # noqa: D102
            data = deepcopy(value)
            data[field] = invalid_data

            with pytest.raises(ValidationError):
                ReceiverReadSchema(**data)


@pytest.mark.parametrize("value", update_param)
class TestReceiverUpdate:  # noqa: D101
    class TestValid:  # noqa: D106
        def test_update(self, value):  # noqa: D102
            result = ReceiverUpdateSchema(**value)
            assert (result.updated_at - datetime.now()).total_seconds() < 5

        def test_partial_update(self, value):  # noqa: D102
            data = deepcopy(value)
            data.pop("name")

            result = ReceiverUpdateSchema(**data)
            assert (result.updated_at - datetime.now()).total_seconds() < 5

    class TestInvalid:  # noqa: D106
        @pytest.mark.parametrize(
            "field, invalid_data",
            invalid,
            ids=lambda f: f"ReceiverUpdate_invalid_{f}",
        )
        def test_update_invalid(self, value, field, invalid_data):  # noqa: D102
            skip_test(field, ["id", "owner_id"])
            data = deepcopy(value)
            data[field] = invalid_data

            with pytest.raises(ValidationError):
                ReceiverUpdateSchema(**data)
