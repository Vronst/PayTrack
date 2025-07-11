import pytest 
from copy import deepcopy
from pydantic import ValidationError 

from .conftest import skip_test
from paytrack.schemas import (
    SubscriptionShareCreateSchema,
    SubscriptionShareReadSchema, 
    SubscriptionShareUpdateSchema
)
from paytrack.constants.subscription_share import MIN_AMOUNT


create_param = [ 
        {
        'amount': 12.5,
        'owner_id': 1,
        'subscription_id': 1,
        }
]

read_param = deepcopy(create_param)
read_param[0]['id'] = 1 

update_param = deepcopy(create_param)
update_param[0].pop('owner_id')

missing_fields = [ 
        'id',
        'amount',
        'owner_id',
        'subscription_id',
]

invalid = [ 
        ('id', 'id'),
        ('amount', 'amount'),
        ('owner_id', 'id'),
        ('subscription_id', 'id'),
]
    

@pytest.mark.parametrize('value', create_param)
class TestSubscriptionShareCreate:

    class TestValid:

        def test_create(self, value):
            SubscriptionShareCreateSchema(**value)

    class TestInvalid:

        @pytest.mark.parametrize(
                'field',
                missing_fields,
                ids=lambda f: f'SubscriptionShareCreate_missing_{f}'
        )
        def test_create_missing(self, value, field):
            skip_test(field, ['id'])
            data = deepcopy(value)
            data.pop(field)

            with pytest.raises(ValidationError):
                SubscriptionShareCreateSchema(**data)

        @pytest.mark.parametrize(
                'field, invalid_data',
                invalid,
                ids=lambda f: f'SubscriptionShareCreate_invalid_{f}'
        )
        def test_create_invalid(self, value, field, invalid_data):
            skip_test(field, ['id'])
            data = deepcopy(value)
            data[field] = invalid_data 

            with pytest.raises(ValidationError):
                SubscriptionShareCreateSchema(**data)

        def test_create_amount_lower_than_min(self, value):
            data = deepcopy(value)
            data['amount'] = MIN_AMOUNT - .1

            with pytest.raises(ValidationError):
                SubscriptionShareCreateSchema(**data)


@pytest.mark.parametrize('value', read_param)
class TestSubscriptionShareRead:

    class TestValid: 

        def test_read(self, value):
            SubscriptionShareReadSchema(**value)

    class TestInvalid: 
        @pytest.mark.parametrize(
                'field',
                missing_fields,
                ids=lambda f: f'SubscriptionShareRead_missing_{f}'
        )
        def test_read_missing(self, value, field):
            data = deepcopy(value)
            data.pop(field)

            with pytest.raises(ValidationError):
                SubscriptionShareReadSchema(**data)

        @pytest.mark.parametrize(
                'field, invalid_data',
                invalid,
                ids=lambda f: f'SubscriptionShareRead_invalid_{f}'
        )
        def test_read_invalid(self, value, field, invalid_data):
            data = deepcopy(value)
            data[field] = invalid_data 

            with pytest.raises(ValidationError):
                SubscriptionShareReadSchema(**data)

        def test_read_amount_lower_than_min(self, value):
            data = deepcopy(value)
            data['amount'] = MIN_AMOUNT - .1

            with pytest.raises(ValidationError):
                SubscriptionShareReadSchema(**data)


@pytest.mark.parametrize('value', update_param)
class TestSubscriptionShareUpdate:

    class TestValid:

        def test_update(self, value):
            SubscriptionShareUpdateSchema(**value)

        @pytest.mark.parametrize(
                'field',
                missing_fields,
                ids=lambda f: f'SubscriptionShareUpdate_partial_{f}'
        )
        def test_partial_update(self, value, field):
            skip_test(field, ['id', 'owner_id'])
            data = deepcopy(value)
            data.pop(field)

            SubscriptionShareUpdateSchema(**data)

    class TestInvalid:

        def test_update_amount_lower_than_min(self, value):
            data = deepcopy(value)
            data['amount'] = MIN_AMOUNT - .1

            with pytest.raises(ValidationError):
                SubscriptionShareUpdateSchema(**data)

        @pytest.mark.parametrize(
                'field, invalid_data',
                invalid,
                ids=lambda f: f'SubscriptionShareUpdate_invalid_{f}'
        )
        def test_update_invalid(self, value, field, invalid_data):
            skip_test(field, ['id', 'owner_id'])
            data = deepcopy(value)
            data[field] = invalid_data 

            with pytest.raises(ValidationError):
                SubscriptionShareUpdateSchema(**data)


