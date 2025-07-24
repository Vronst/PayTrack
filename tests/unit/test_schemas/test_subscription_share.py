from copy import deepcopy  # noqa: D100

import pytest
from pydantic import ValidationError

from paytrack.constants.subscription_share import MIN_AMOUNT
from paytrack.schemas import (
    SubscriptionShareCreateSchema,
    SubscriptionShareReadSchema,
    SubscriptionShareUpdateSchema,
)

from .conftest import skip_test

create_param = [
    {
        "amount": 12.5,
        "owner_id": 1,
        "subscription_id": 1,
    }
]

read_param = deepcopy(create_param)
read_param[0]["id"] = 1

update_param = deepcopy(create_param)
update_param[0].pop("owner_id")

missing_fields = [
    "id",
    "amount",
    "owner_id",
    "subscription_id",
]

invalid = [
    ("id", "id"),
    ("amount", "amount"),
    ("owner_id", "id"),
    ("subscription_id", "id"),
]


@pytest.mark.parametrize("value", create_param)
class TestSubscriptionShareCreate:  # noqa: D101
    class TestValid:  # noqa: D106
        def test_create(self, value):  # noqa: D102
            SubscriptionShareCreateSchema(**value)

    class TestInvalid:  # noqa: D106
        @pytest.mark.parametrize(
            "field",
            missing_fields,
            ids=lambda f: f"SubscriptionShareCreate_missing_{f}",
        )
        def test_create_missing(self, value, field):  # noqa: D102
            skip_test(field, ["id"])
            data = deepcopy(value)
            data.pop(field)

            with pytest.raises(ValidationError):
                SubscriptionShareCreateSchema(**data)

        @pytest.mark.parametrize(
            "field, invalid_data",
            invalid,
            ids=lambda f: f"SubscriptionShareCreate_invalid_{f}",
        )
        def test_create_invalid(self, value, field, invalid_data):  # noqa: D102
            skip_test(field, ["id"])
            data = deepcopy(value)
            data[field] = invalid_data

            with pytest.raises(ValidationError):
                SubscriptionShareCreateSchema(**data)

        def test_create_amount_lower_than_min(self, value):  # noqa: D102
            data = deepcopy(value)
            data["amount"] = MIN_AMOUNT - 0.1

            with pytest.raises(ValidationError):
                SubscriptionShareCreateSchema(**data)


@pytest.mark.parametrize("value", read_param)
class TestSubscriptionShareRead:  # noqa: D101
    class TestValid:  # noqa: D106
        def test_read(self, value):  # noqa: D102
            SubscriptionShareReadSchema(**value)

    class TestInvalid:  # noqa: D106
        @pytest.mark.parametrize(
            "field",
            missing_fields,
            ids=lambda f: f"SubscriptionShareRead_missing_{f}",
        )
        def test_read_missing(self, value, field):  # noqa: D102
            data = deepcopy(value)
            data.pop(field)

            with pytest.raises(ValidationError):
                SubscriptionShareReadSchema(**data)

        @pytest.mark.parametrize(
            "field, invalid_data",
            invalid,
            ids=lambda f: f"SubscriptionShareRead_invalid_{f}",
        )
        def test_read_invalid(self, value, field, invalid_data):  # noqa: D102
            data = deepcopy(value)
            data[field] = invalid_data

            with pytest.raises(ValidationError):
                SubscriptionShareReadSchema(**data)

        def test_read_amount_lower_than_min(self, value):  # noqa: D102
            data = deepcopy(value)
            data["amount"] = MIN_AMOUNT - 0.1

            with pytest.raises(ValidationError):
                SubscriptionShareReadSchema(**data)


@pytest.mark.parametrize("value", update_param)
class TestSubscriptionShareUpdate:  # noqa: D101
    class TestValid:  # noqa: D106
        def test_update(self, value):  # noqa: D102
            SubscriptionShareUpdateSchema(**value)

        @pytest.mark.parametrize(
            "field",
            missing_fields,
            ids=lambda f: f"SubscriptionShareUpdate_partial_{f}",
        )
        def test_partial_update(self, value, field):  # noqa: D102
            skip_test(field, ["id", "owner_id"])
            data = deepcopy(value)
            data.pop(field)

            SubscriptionShareUpdateSchema(**data)

    class TestInvalid:  # noqa: D106
        def test_update_amount_lower_than_min(self, value):  # noqa: D102
            data = deepcopy(value)
            data["amount"] = MIN_AMOUNT - 0.1

            with pytest.raises(ValidationError):
                SubscriptionShareUpdateSchema(**data)

        @pytest.mark.parametrize(
            "field, invalid_data",
            invalid,
            ids=lambda f: f"SubscriptionShareUpdate_invalid_{f}",
        )
        def test_update_invalid(self, value, field, invalid_data):  # noqa: D102
            skip_test(field, ["id", "owner_id"])
            data = deepcopy(value)
            data[field] = invalid_data

            with pytest.raises(ValidationError):
                SubscriptionShareUpdateSchema(**data)
