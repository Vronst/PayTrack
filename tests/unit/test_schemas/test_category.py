from copy import deepcopy  # noqa: D100

import pytest
from pydantic import ValidationError

from paytrack.schemas import (
    CategoryCreateSchema,
    CategoryReadSchema,
    CategoryUpdateSchema,
)
from paytrack.services.date import utc_now

from .conftest import skip_test

create_params = [
    {
        "root_category": None,
        "name": None,
        "custom": False,
    },
    {
        "root_category": 1,
        "name": None,
        "custom": False,
    },
    {
        "root_category": 1,
        "name": "name",
        "custom": True,
    },
    {
        "root_category": None,
        "name": "name",
        "custom": True,
    },
]

read_params = deepcopy(create_params)
for param in read_params:
    param["id"] = 1
    param["subcategories"] = []

update_params = deepcopy(create_params)
for param in update_params:
    param.pop("custom")

missing_fields = [
    "root_category",
    "name",
    "custom",
    "subcategories",
    "id",
]

invalid = [
    ("id", "id"),
    ("root_category", "root"),
    (
        "name",
        1,
    ),
    ("custom", "custom"),
    ("subcategories", "subcategories"),
]


@pytest.mark.parametrize("value", create_params)
class TestCategoryCreate:  # noqa: D101
    class TestValid:  # noqa: D106
        def test_creation(self, value):  # noqa: D102
            CategoryCreateSchema(**value)

    class TestInvalid:  # noqa: D106
        @pytest.mark.parametrize(
            "field",
            missing_fields,
            ids=lambda f: f"CategoryCreate_missing_{f}",
        )
        def test_create_missing(self, value, field):  # noqa: D102
            skip_test(
                field,
                ["id", "subcategories", "custom", "name", "root_category"],
            )
            data = deepcopy(value)
            data.pop(field)

            with pytest.raises(ValidationError):
                CategoryCreateSchema(**data)

        @pytest.mark.parametrize(
            "field, invalid_data",
            invalid,
            ids=lambda f: f"CategoryCreate_invalid_{f}",
        )
        def test_create_invalid(self, value, field, invalid_data):  # noqa: D102
            skip_test(field, ["id", "subcategories"])
            data = deepcopy(value)
            data[field] = invalid_data

            with pytest.raises(ValidationError):
                CategoryCreateSchema(**data)


@pytest.mark.parametrize("value", read_params)
class TestCategoryRead:  # noqa: D101
    class TestValid:  # noqa: D106
        def test_read(self, value):  # noqa: D102
            CategoryReadSchema(**value)

    class TestInvalid:  # noqa: D106
        @pytest.mark.parametrize(
            "field", missing_fields, ids=lambda f: f"CategoryRead_missing_{f}"
        )
        def test_read_missing(self, value, field):  # noqa: D102
            skip_test(field, ["custom", "name", "root_category"])
            data = deepcopy(value)
            data.pop(field)

            with pytest.raises(ValidationError):
                CategoryReadSchema(**data)

        @pytest.mark.parametrize(
            "field, invalid_data",
            invalid,
            ids=lambda f: f"CategoryRead_invalid_{f}",
        )
        def test_read_invalid(self, value, field, invalid_data):  # noqa: D102
            data = deepcopy(value)
            data[field] = invalid_data

            with pytest.raises(ValidationError):
                CategoryReadSchema(**data)


@pytest.mark.parametrize("value", update_params)
class TestCategoryUpdate:  # noqa: D101
    class TestValid:  # noqa: D106
        def test_update(self, value):  # noqa: D102
            result = CategoryUpdateSchema(**value)

            assert (result.updated_at - utc_now()).total_seconds() < 5

        @pytest.mark.regression
        @pytest.mark.parametrize(
            "field",
            missing_fields,
            ids=lambda f: f"CategoryUpdate_missing_{f}",
        )
        def test_partial_update(self, value, field):  # noqa: D102
            skip_test(field, ["id", "custom", "subcategories"])
            data = deepcopy(value)
            data.pop(field)

            result = CategoryUpdateSchema(**data)

            assert (result.updated_at - utc_now()).total_seconds() < 5

    class TestInvalid:  # noqa: D106
        @pytest.mark.parametrize(
            "field, invalid_data",
            invalid,
            ids=lambda f: f"CategoryUpdate_invalid_{f}",
        )
        def test_update_invalid(self, value, field, invalid_data):  # noqa: D102
            skip_test(field, ["custom", "id", "subcategories"])
            data = deepcopy(value)
            data[field] = invalid_data

            with pytest.raises(ValidationError):
                CategoryUpdateSchema(**data)
