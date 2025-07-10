from copy import deepcopy
from datetime import datetime
from pydantic import ValidationError
import pytest
from .conftest import skip_test
from paytrack.schemas import CurrencyCreateSchema, CurrencyReadSchema, CurrencyUpdateSchema 




create_param = [ 
        {
        'code': 'PLN',
        'name': 'Złoty',
        'value': 12.5
        }
]

read_param = deepcopy(create_param)
read_param[0]['id'] = 1 

update_param = deepcopy(create_param)

missing_fields = [ 
        'code',
        'id',
        'name',
        'value',
]

invalid = [ 
        ('code', 1),
        ('name', 2),
        ('value', 'value'),
        ('id', 'id'),
]


@pytest.mark.parametrize('value', create_param)
class TestCurrencyCreate:

    class TestValid:
        def test_creation(self, value):

            CurrencyCreateSchema(**value)

    class TestInvalid:

        @pytest.mark.parametrize(
                'field',
                missing_fields,
                ids=lambda f: f"CurrencyCreate_missing_{f}")
        def test_create_missing(self, value, field):
            skip_test(field, ['id'])

            data = deepcopy(value)
            data.pop(field)

            with pytest.raises(ValidationError):
                CurrencyCreateSchema(**data)

        @pytest.mark.parametrize(
                'field, invalid_data',
                invalid,
                ids=lambda f: f'CurrencyCreate_invalid_{f}')
        def test_create_invalid_data(self, value, field, invalid_data):
            skip_test(field, ['id'])

            data = deepcopy(value)
            data[field] = invalid_data 

            with pytest.raises(ValidationError):
                CurrencyCreateSchema(**data)


@pytest.mark.parametrize('value', read_param)
class TestCurrencyRead:

    class TestValid:
        def test_read(self, value):

            CurrencyReadSchema(**value)

    class TestInvalid:
        @pytest.mark.parametrize(
                'field',
                missing_fields,
                ids=lambda f: f"CurrencyRead_missing_{f}")
        def test_read_missing(self, value, field):
            data = deepcopy(value)
            data.pop(field)

            with pytest.raises(ValidationError):
                CurrencyReadSchema(**data)

        @pytest.mark.parametrize(
                'field, invalid_data',
                invalid,
                ids=lambda f: f'CurrencyRead_invalid_{f}')
        def test_read_invalid_data(self, value, field, invalid_data):
            data = deepcopy(value)
            data[field] = invalid_data 

            with pytest.raises(ValidationError):
                CurrencyReadSchema(**data)


@pytest.mark.parametrize('value', update_param)
class TestCurrencyUpdate:

    class TestValid:
        def test_update(self, value):

            result = CurrencyUpdateSchema(**value)
            assert (result.updated_at - datetime.now()).total_seconds() < 5

        @pytest.mark.parametrize(
                'field',
                missing_fields,
                ids=lambda f: f"CurrencyUpdate_missing_{f}")
        def test_partial_update(self, value, field):
            skip_test(field, ['id'])
            data = deepcopy(value)
            data.pop(field)

            result = CurrencyUpdateSchema(**data)
            assert (result.updated_at - datetime.now()).total_seconds() < 5

    class TestInvalid:
        @pytest.mark.parametrize(
                'field, invalid_data',
                invalid,
                ids=lambda f: f'CurrencyUpdate_invalid_{f}')
        def test_update_invalid_data(self, value, field, invalid_data):
            skip_test(field, ['id'])
            data = deepcopy(value)
            data[field] = invalid_data 

            with pytest.raises(ValidationError):
                CurrencyUpdateSchema(**data)


