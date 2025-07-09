from copy import deepcopy
from datetime import datetime
import pytest 
from pydantic import ValidationError 

from paytrack.schemas import SubscriptionCreateSchema, SubscriptionReadSchema, SubscriptionUpdateSchema 
from paytrack.constants.subscription import PERIOD_CHOICES, MIN_AMOUNT


create_param = [{
    'name': 'name',
    'amount': 12.5, 
    'currency_id': 1,
    'period': PERIOD_CHOICES[0],
    'shared': False,
    'active': True,
    'date': datetime.now().date(),
    'owner_id': 1
}
    ]

read_param = deepcopy(create_param)
read_param[0]['id'] = 1 
read_param[0]['included'] = []
read_param[0]['subscription_share'] = []

update_param = deepcopy(create_param)
update_param[0].pop('owner_id')

missing_fields = [
            'name',
            'amount', 
            'currency_id', 
            'id', 
            'period', 
            'shared',
            'active',
            'date', 
            'owner_id'
                   ]

invalid_values = [ 
    ('name', 10),
    ('amount', 'amount'),
    ('currency_id', 'id'),
    ('id', 'id'),
    ('period', 'invalid period'),
    ('shared', 10),
    ('active', 10),
    ('date', 'invalid date'),
    ('owner_id', 'id')
]


class TestSubscriptionCreate:
    class TestValid:

        @pytest.mark.parametrize('value', create_param)
        def test_create(self, value):
            SubscriptionCreateSchema(**value)

    class TestInvalid:

        @pytest.mark.parametrize('value', create_param)
        @pytest.mark.parametrize('field', missing_fields, ids=lambda f: f'missing_{f}')
        def test_missing_field(self, field, value):
            if field == 'id':
                return
            data = deepcopy(value)
            data.pop(field)
            
            with pytest.raises(ValidationError):
                SubscriptionCreateSchema(**data)

        @pytest.mark.parametrize('value', create_param)
        def test_create_amount_below_lower(self, value):
            data = deepcopy(value)
            data['amount'] = MIN_AMOUNT - .1

            with pytest.raises(ValidationError):
                SubscriptionCreateSchema(**data)

        @pytest.mark.parametrize('value', create_param)
        @pytest.mark.parametrize('field,data',
                                 invalid_values,
                                 ids=lambda f: f'invalid_{f}')
        def test_create_invalid_data(self, value, field, data):
            data = deepcopy(value)
            if field == 'id':
                return
            data[field] = data

            with pytest.raises(ValidationError):
                SubscriptionCreateSchema(**data)


class TestSubscriptionRead:
    class TestValid:

        @pytest.mark.parametrize('value', read_param)
        def test_read(self, value):
            SubscriptionReadSchema(**value) 

    class TestInvalid:

        @pytest.mark.parametrize('value', read_param)
        @pytest.mark.parametrize('field', missing_fields, ids=lambda f: f'missing_{f}')
        def test_missing_field(self, field, value):
            data = deepcopy(value)
            data.pop(field)
            
            with pytest.raises(ValidationError):
                SubscriptionReadSchema(**data)

        @pytest.mark.parametrize('value', create_param)
        @pytest.mark.parametrize('field,data',
                                 invalid_values,
                                 ids=lambda f: f'invalid_{f}')
        def test_create_invalid_data(self, value, field, data):
            data = deepcopy(value)
            data[field] = data

            with pytest.raises(ValidationError):
                SubscriptionReadSchema(**data)


class TestSubscriptionUpdate:

    class TestValid:
        
        @pytest.mark.parametrize('value', update_param)
        def test_update(self, value):
            SubscriptionUpdateSchema(**value)

        @pytest.mark.parametrize('value', update_param)
        def test_partial_update(self, value):
            data = deepcopy(value)
            data.pop('shared')
            data.pop('currency_id')
            data.pop('name')

            SubscriptionUpdateSchema(**data)

    class TestInvalid:

        @pytest.mark.parametrize('value', update_param)
        def test_update_name_int(self, value):
            data = deepcopy(value)
            data['name'] = 10

            with pytest.raises(ValidationError):
                SubscriptionUpdateSchema(**data)
            
        @pytest.mark.parametrize('value', create_param)
        @pytest.mark.regression
        @pytest.mark.parametrize('field,data',
                                 invalid_values,
                                 ids=lambda f: f'invalid_{f}')
        def test_create_invalid_data(self, value, field, data):
            if field in ['id', 'owner_id']:
                return
            data = deepcopy(value)
            data[field] = data

            with pytest.raises(ValidationError):
                SubscriptionUpdateSchema(**data)

