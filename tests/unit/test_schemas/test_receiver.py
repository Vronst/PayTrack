from copy import deepcopy
from datetime import datetime
from pydantic import ValidationError
import pytest

from .conftest import skip_test
from paytrack.schemas import ReceiverCreateSchema, ReceiverReadSchema, ReceiverUpdateSchema


create_param = [ 
        {
        'owner_id': 1,
        'name': 'name'
        }
]

read_param = deepcopy(create_param)
read_param[0]['id'] = 1
read_param[0]['included'] = []

update_param = deepcopy(create_param)
update_param[0].pop('owner_id')
update_param[0]['included'] = []

missing_field = [ 
        'owner_id',
        'name',
        'included'
]

invalid = [ 
        ('owner_id', 'owner_id'),
        ('name', 2),
        ('included', 'included')
]


@pytest.mark.parametrize('value', create_param)
class TestReceiverCreate:

    class TestValid:
        def test_create(self, value):
            
            ReceiverCreateSchema(**value)

    class TestInvalid:

        @pytest.mark.parametrize(
            'field',
            missing_field,
            ids=lambda f: f"ReceiverCreate_missing_field_{f}"
        )
        def test_create_missing_field(self, value, field):
            skip_test(field, ['included'])
            data = deepcopy(value)
            data.pop(field)

            with pytest.raises(ValidationError):
                ReceiverCreateSchema(**data)

        @pytest.mark.parametrize(
                'field, invalid_data',
                invalid,
            ids=lambda f: f'ReceiverCreate_missing_field_{f}'
        )
        def test_create_invalid_data(self, value, field, invalid_data):
            skip_test(field, ['included'])
            data = deepcopy(value)
            data[field] = invalid_data 

            with pytest.raises(ValidationError):
                ReceiverCreateSchema(**data)


@pytest.mark.parametrize('value', read_param)
class TestReceiverRead:

    class TestValid:
        def test_read(self, value):
            
            ReceiverReadSchema(**value)

    class TestInvalid:

        @pytest.mark.parametrize(
                'field',
                missing_field,
                ids=lambda f: f'ReceiverRead_missing_field_{f}'
        )
        def test_read_missing_field(self, value, field):
            data = deepcopy(value)
            data.pop(field)

            with pytest.raises(ValidationError):
                ReceiverReadSchema(**data)

        @pytest.mark.parametrize(
                'field, invalid_data', 
                invalid,
                ids=lambda f: f'ReceiverRead_invalid_{f}'
        )
        def test_read_invalid_data(self, value, field, invalid_data):
            data = deepcopy(value)
            data[field] = invalid_data 

            with pytest.raises(ValidationError):
                ReceiverReadSchema(**data)


@pytest.mark.parametrize('value', update_param)
class TestReceiverUpdate:

    class TestValid:

        def test_update(self, value):
            
            result = ReceiverUpdateSchema(**value)
            assert (result.updated_at - datetime.now()).total_seconds() < 5

        def test_partial_update(self, value):
            data = deepcopy(value)
            data.pop('name')
            
            result = ReceiverUpdateSchema(**data)
            assert (result.updated_at - datetime.now()).total_seconds() < 5


    class TestInvalid:

        @pytest.mark.parametrize(
                'field, invalid_data',
                invalid,
                ids=lambda f: f"ReceiverUpdate_invalid_{f}")
        def test_update_invalid(self, value, field, invalid_data):
            skip_test(field, ['id', 'owner_id'])
            data = deepcopy(value)
            data[field] = invalid_data

            with pytest.raises(ValidationError):
                ReceiverUpdateSchema(**data)



