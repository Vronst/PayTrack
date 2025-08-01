from copy import deepcopy  # noqa: D100

import pytest
from pydantic import ValidationError

from paytrack.constants.transaction_share import MIN_AMOUNT
from paytrack.schemas import (
    TransactionShareCreateSchema,
    TransactionShareReadSchema,
    TransactionShareUpdateSchema,
)

from .conftest import skip_test

create_param = [
    {
        "owner_id": 1,
        "amount": MIN_AMOUNT + 0.1,
        "transaction_id": 1,
    }
]

read_param = deepcopy(create_param)
read_param[0]["id"] = 1

update_param = deepcopy(create_param)
update_param[0].pop("owner_id")

missing_fields = [
    "owner_id",
    "id",
    "amount",
    "transaction_id",
]

invalid = [
    ("id", "id"),
    ("amount", "amount"),
    ("transaction_id", "transaction_id"),
    ("amount", MIN_AMOUNT - 0.1),
]


@pytest.mark.parametrize("value", create_param)
class TestTransactionCreateShare:  # noqa: D101
    class TestValid:  # noqa: D106
        def test_create(self, value):  # noqa: D102
            TransactionShareCreateSchema(**value)

    class TestInvalid:  # noqa: D106
        @pytest.mark.parametrize(
            "field",
            missing_fields,
            ids=lambda f: f"TransactionShareCreate_missing_{f}",
        )
        def test_create_missing(self, value, field):  # noqa: D102
            skip_test(field, ["id"])
            data = deepcopy(value)
            data.pop(field)

            with pytest.raises(ValidationError):
                TransactionShareCreateSchema(**data)

        @pytest.mark.parametrize(
            "field, invalid_data",
            invalid,
            ids=lambda f: f"TransactionShareCreate_invalid_{f}",
        )
        def test_create_invalid(self, value, field, invalid_data):  # noqa: D102
            skip_test(field, ["id"])
            data = deepcopy(value)
            data[field] = invalid_data

            with pytest.raises(ValidationError):
                TransactionShareCreateSchema(**data)


@pytest.mark.parametrize("value", read_param)
class TestTransactionReadShare:  # noqa: D101
    class TestValid:  # noqa: D106
        def test_read(self, value):  # noqa: D102
            TransactionShareReadSchema(**value)

    class TestInvalid:  # noqa: D106
        @pytest.mark.parametrize(
            "field",
            missing_fields,
            ids=lambda f: f"TransactionShareRead_missing_{f}",
        )
        def test_read_missing(self, value, field):  # noqa: D102
            data = deepcopy(value)
            data.pop(field)

            with pytest.raises(ValidationError):
                TransactionShareReadSchema(**data)

        @pytest.mark.parametrize(
            "field, invalid_data",
            invalid,
            ids=lambda f: f"TransactionShareRead_invalid_{f}",
        )
        def test_read_invalid(self, value, field, invalid_data):  # noqa: D102
            data = deepcopy(value)
            data[field] = invalid_data

            with pytest.raises(ValidationError):
                TransactionShareReadSchema(**data)


@pytest.mark.parametrize("value", update_param)
class TestTransactionUpdateShare:  # noqa: D101
    class TestValid:  # noqa: D106
        def test_update(self, value):  # noqa: D102
            TransactionShareUpdateSchema(**value)

        @pytest.mark.parametrize(
            "field",
            missing_fields,
            ids=lambda f: f"TransactionShareUpdate_partial_missing_{f}",
        )
        def test_partial_update(self, value, field):  # noqa: D102
            skip_test(field, ["id", "owner_id"])
            data = deepcopy(value)
            data.pop(field)

            TransactionShareUpdateSchema(**data)

    class TestInvalid:  # noqa: D106
        @pytest.mark.parametrize(
            "field, invalid_data",
            invalid,
            ids=lambda f: f"TransactionShareUpdate_invalid_{f}",
        )
        def test_update_invalid(self, value, field, invalid_data):  # noqa: D102
            skip_test(field, ["id", "owner_id"])
            data = deepcopy(value)
            data[field] = invalid_data

            with pytest.raises(ValidationError):
                TransactionShareUpdateSchema(**data)
