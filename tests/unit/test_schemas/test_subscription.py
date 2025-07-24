from copy import deepcopy  # noqa: D100
from datetime import datetime

import pytest
from pydantic import ValidationError

from paytrack.constants.subscription import MIN_AMOUNT, PERIOD_CHOICES
from paytrack.schemas import (
    SubscriptionCreateSchema,
    SubscriptionReadSchema,
    SubscriptionUpdateSchema,
)
from paytrack.services.date import utc_now

from .conftest import skip_test

create_param = [
    {
        "name": "name",
        "amount": 12.5,
        "currency_id": 1,
        "period": PERIOD_CHOICES[0],
        "shared": False,
        "active": True,
        "date": datetime.now().date(),
        "owner_id": 1,
    }
]

read_param = deepcopy(create_param)
read_param[0]["id"] = 1
read_param[0]["included"] = []
read_param[0]["subscription_share"] = []

update_param = deepcopy(create_param)
update_param[0].pop("owner_id")

missing_fields = [
    "name",
    "amount",
    "currency_id",
    "id",
    "period",
    "shared",
    "active",
    "date",
    "owner_id",
]

invalid_values = [
    ("name", 10),
    ("amount", "amount"),
    ("currency_id", "id"),
    ("id", "id"),
    ("period", "invalid period"),
    ("shared", 10),
    ("active", 10),
    ("date", "invalid date"),
    ("owner_id", "id"),
]


@pytest.mark.parametrize("value", create_param)
class TestSubscriptionCreate:  # noqa: D101
    class TestValid:  # noqa: D106
        def test_create(self, value):  # noqa: D102
            SubscriptionCreateSchema(**value)

    class TestInvalid:  # noqa: D106
        @pytest.mark.parametrize(
            "field",
            missing_fields,
            ids=lambda f: f"SubscriptionCreaet_missing_{f}",
        )
        def test_missing_field(self, field, value):  # noqa: D102
            skip_test(field, ["id"])
            data = deepcopy(value)
            data.pop(field)

            with pytest.raises(ValidationError):
                SubscriptionCreateSchema(**data)

        def test_create_amount_below_lower(self, value):  # noqa: D102
            data = deepcopy(value)
            data["amount"] = MIN_AMOUNT - 0.1

            with pytest.raises(ValidationError):
                SubscriptionCreateSchema(**data)

        @pytest.mark.parametrize(
            "field,data",
            invalid_values,
            ids=lambda f: f"SubscriptionCreate_invalid_value_{f}",
        )
        def test_create_invalid_data(self, value, field, data):  # noqa: D102
            data = deepcopy(value)
            skip_test(field, ["id"])
            data[field] = data

            with pytest.raises(ValidationError):
                SubscriptionCreateSchema(**data)


@pytest.mark.parametrize("value", read_param)
class TestSubscriptionRead:  # noqa: D101
    class TestValid:  # noqa: D106
        def test_read(self, value):  # noqa: D102
            SubscriptionReadSchema(**value)

    class TestInvalid:  # noqa: D106
        @pytest.mark.parametrize(
            "field",
            missing_fields,
            ids=lambda f: f"SubscriptionRead_missing_{f}",
        )
        def test_missing_field(self, field, value):  # noqa: D102
            data = deepcopy(value)
            data.pop(field)

            with pytest.raises(ValidationError):
                SubscriptionReadSchema(**data)

        @pytest.mark.parametrize(
            "field,data",
            invalid_values,
            ids=lambda f: f"SubscriptionRead_invalid_values_{f}",
        )
        def test_create_invalid_data(self, value, field, data):  # noqa: D102
            data = deepcopy(value)
            data[field] = data

            with pytest.raises(ValidationError):
                SubscriptionReadSchema(**data)


@pytest.mark.parametrize("value", update_param)
class TestSubscriptionUpdate:  # noqa: D101
    class TestValid:  # noqa: D106
        def test_update(self, value):  # noqa: D102
            result = SubscriptionUpdateSchema(**value)
            assert (result.updated_at - utc_now()).total_seconds() < 5

        def test_partial_update(self, value):  # noqa: D102
            data = deepcopy(value)
            data.pop("shared")
            data.pop("currency_id")
            data.pop("name")

            result = SubscriptionUpdateSchema(**data)
            assert (result.updated_at - utc_now()).total_seconds() < 5

    class TestInvalid:  # noqa: D106
        def test_update_name_int(self, value):  # noqa: D102
            data = deepcopy(value)
            data["name"] = 10

            with pytest.raises(ValidationError):
                SubscriptionUpdateSchema(**data)

        @pytest.mark.regression
        @pytest.mark.parametrize(
            "field,data",
            invalid_values,
            ids=lambda f: f"SubscriptionUpdate_invalid_value_{f}",
        )
        def test_create_invalid_data(self, value, field, data):  # noqa: D102
            skip_test(field, ["id", "owner_id"])
            data = deepcopy(value)
            data[field] = data

            with pytest.raises(ValidationError):
                SubscriptionUpdateSchema(**data)
