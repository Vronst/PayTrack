from copy import deepcopy  # noqa: D100

import pytest
from pydantic import ValidationError

from paytrack.constants.translation import WORD_LENGTH
from paytrack.schemas import (
    TranslationCreateSchema,
    TranslationReadSchema,
    TranslationUpdateSchema,
)

from .conftest import skip_test

create_param = [
    {
        "category_id": 1,
        "language_id": 1,
        "word": "a" * WORD_LENGTH,
    }
]

read_param = deepcopy(create_param)
read_param[0]["id"] = 1

update_param = deepcopy(create_param)

missing_fields = [
    "category_id",
    "id",
    "language_id",
    "word",
]

invalid = [
    ("id", "id"),
    ("language_id", "id"),
    ("word", "a" * WORD_LENGTH + "a"),
]


@pytest.mark.parametrize("value", create_param)
class TestTranslationCreate:  # noqa: D101
    class TestValid:  # noqa: D106
        def test_create(self, value):  # noqa: D102
            TranslationCreateSchema(**value)

    class TestInvalid:  # noqa: D106
        @pytest.mark.parametrize(
            "field",
            missing_fields,
            ids=lambda f: f"TranslationCreate_missing_{f}",
        )
        def test_create_missing(self, value, field):  # noqa: D102
            skip_test(field, ["id"])
            data = deepcopy(value)
            data.pop(field)

            with pytest.raises(ValidationError):
                TranslationCreateSchema(**data)

        @pytest.mark.parametrize(
            "field, invalid_data",
            invalid,
            ids=lambda f: f"TranslationCreate_invalid_{f}",
        )
        def test_create_invalid(self, value, field, invalid_data):  # noqa: D102
            skip_test(field, ["id"])
            data = deepcopy(value)
            data[field] = invalid_data

            with pytest.raises(ValidationError):
                TranslationCreateSchema(**data)


@pytest.mark.parametrize("value", read_param)
class TestTranslationRead:  # noqa: D101
    class TestValid:  # noqa: D106
        def test_read(self, value):  # noqa: D102
            TranslationReadSchema(**value)

    class TestInvalid:  # noqa: D106
        @pytest.mark.parametrize(
            "field",
            missing_fields,
            ids=lambda f: f"TranslationRead_missing_{f}",
        )
        def test_read_missing(self, value, field):  # noqa: D102
            data = deepcopy(value)
            data.pop(field)

            with pytest.raises(ValidationError):
                TranslationReadSchema(**data)

        @pytest.mark.parametrize(
            "field, invalid_data",
            invalid,
            ids=lambda f: f"TranslationRead_invalid_{f}",
        )
        def test_read_invalid(self, value, field, invalid_data):  # noqa: D102
            data = deepcopy(value)
            data[field] = invalid_data

            with pytest.raises(ValidationError):
                TranslationReadSchema(**data)


@pytest.mark.parametrize("value", update_param)
class TestTranslationUpdate:  # noqa: D101
    class TestValid:  # noqa: D106
        def test_update(self, value):  # noqa: D102
            TranslationUpdateSchema(**value)

        @pytest.mark.parametrize(
            "field",
            missing_fields,
            ids=lambda f: f"TranslationUpdate_partial_missing_{f}",
        )
        def test_partial_update(self, value, field):  # noqa: D102
            skip_test(field, ["id"])
            data = deepcopy(value)
            data.pop(field)

            TranslationUpdateSchema(**data)

    class TestInvalid:  # noqa: D106
        @pytest.mark.parametrize(
            "field, invalid_data",
            invalid,
            ids=lambda f: f"TranslationRead_invalid_{f}",
        )
        def test_update_invalid(self, value, field, invalid_data):  # noqa: D102
            skip_test(field, ["id"])
            data = deepcopy(value)
            data[field] = invalid_data

            with pytest.raises(ValidationError):
                TranslationUpdateSchema(**data)
