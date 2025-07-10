from copy import deepcopy
from datetime import datetime
from pydantic import ValidationError
import pytest
from .conftest import skip_test
from paytrack.schemas import LanguageCreateSchema, LanguageReadSchema, LanguageUpdateSchema

create_param: list[dict] = [ 
        {
        'language_code': 'PL',
        'language_name': 'Polski'
        }
]

read_param = deepcopy(create_param)
read_param[0]['id'] = 1

update_param = deepcopy(create_param)

missing_fields = [ 
        'language_name',
        'language_code',
        'id',
]

invalid = [ 
        ('id', 'id'),
        ('language_code', 1),
        ('language_name', 2),
]


@pytest.mark.parametrize('value', create_param)
class TestLangaugeCreate:

    class TestValid:
        def test_create(self, value):

            LanguageCreateSchema(**value)

    class TestInvalid:
        
        @pytest.mark.parametrize(
                'field', 
                missing_fields,
                ids=lambda f: f"LanguageCreate_missing_{f}"
        )
        def test_create_missing_field(self, value, field):
            skip_test(field, ['id'])
            data = deepcopy(value)
            data.pop(field)

            with pytest.raises(ValidationError):
                LanguageCreateSchema(**data)

        @pytest.mark.parametrize(
                'field, invalid_data',
                invalid,
                ids=lambda f: f'LanguageCreate_invalid_{f}'
        )
        def test_create_invalid_data(self, value, field, invalid_data):
            skip_test(field, ['id'])
            data = deepcopy(value)
            data[field] = invalid_data 

            with pytest.raises(ValidationError):
                LanguageCreateSchema(**data)


@pytest.mark.parametrize('value', read_param)
class TestLangaugeRead:

    class TestValid: 

        def test_read(self, value):

            LanguageReadSchema(**value)

    class TestInvalid:

        @pytest.mark.parametrize(
                'field', 
                missing_fields,
                ids=lambda f: f"LanguageRead_missing_{f}"
        )
        def test_read_missing_field(self, value, field):
            data = deepcopy(value)
            data.pop(field)

            with pytest.raises(ValidationError):
                LanguageReadSchema(**data)

        @pytest.mark.parametrize(
                'field, invalid_data',
                invalid,
                ids=lambda f: f'LanguageRead_invalid_{f}'
        )
        def test_read_invalid_data(self, value, field, invalid_data):
            data = deepcopy(value)
            data[field] = invalid_data 

            with pytest.raises(ValidationError):
                LanguageReadSchema(**data)


@pytest.mark.parametrize('value', update_param)
class TestLangaugeUpdate:

    class TestValid:
        def test_update(self, value):

            result = LanguageUpdateSchema(**value)
            assert (result.updated_at - datetime.now()).total_seconds() < 5

        def test_partial_update(self, value):
            data = deepcopy(value)
            data.pop('language_code')

            result = LanguageUpdateSchema(**data)
            assert (result.updated_at - datetime.now()).total_seconds() < 5

    class TestInvalid:
        @pytest.mark.parametrize(
                'field, invalid_data',
                invalid,
                ids=lambda f: f'LanguageRead_invalid_{f}'
        )
        def test_update_invalid_data(self, value, field, invalid_data):
            skip_test(field, ['id'])
            data = deepcopy(value)
            data[field] = invalid_data 

            with pytest.raises(ValidationError):
                LanguageUpdateSchema(**data)


