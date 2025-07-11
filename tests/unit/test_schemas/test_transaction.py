import pytest 
from datetime import datetime
from pydantic import ValidationError 
from copy import deepcopy 

from paytrack.constants.transaction import MIN_AMOUNT, TYPE_CHOICE 
from paytrack.schemas import ( 
        TransactionCreateSchema,
        TransactionReadSchema, 
        TransactionUpdateSchema,
)
from .conftest import skip_test
    

create_params = [ 
        {
        'date': datetime.now().date(),
        'done': False,
        'owner_id': 1,
        'category_id': 1,
        'receiver_id': None,
        'type': TYPE_CHOICE[0],
        'amount': MIN_AMOUNT + .1,
        'currency_id': 1,
        'receiver_name': 'receiver',
        },
        {
        'date': '1999-01-28',
        'done': True,
        'owner_id': 12,
        'category_id': 11,
        'receiver_id': 1,
        'type': TYPE_CHOICE[0],
        'amount': MIN_AMOUNT + 1,
        'currency_id': 1,
        'receiver_name': None,
        },
]

read_param = deepcopy(create_params)
for param in read_param:
    param['id'] = 1 

update_param = deepcopy(create_params)
for param in update_param:
    param.pop('owner_id') 

invalid = [ 
        ('date', '28.01.1999'),
        ('done', 'invalid'),
        ('owner_id', 'owner_id'),
        ('category_id', 'category_id'),
        ('receiver_id', 'receiver_id'),
        ('type', 'invalid type'),
        ('amount', 'amount'),
        ('amount', MIN_AMOUNT - 1),
        ('currency_id', 'currency_id'),
        ('receiver_name', 2),
]

missing_fields = [ 
        'date',
        'done', 
        'owner_id',
        'category_id',
        'receiver_id',
        'type', 
        'amount',
        'id',
        'currency_id',
        'receiver_name',
]


@pytest.mark.parametrize('value', create_params)
class TestTransactionCreateSchema:

    class TestValid:

        def test_create(self, value):
            TransactionCreateSchema(**value)


    class TestInvalid:

        @pytest.mark.parametrize(
                'field',
                missing_fields,
                ids=lambda f: f'TransactionCreate_missing_{f}'
        )
        def test_creat_missing(self, value, field):
            skip_test(field, ['id', 'receiver_id', 'receiver_name'])
            data = deepcopy(value)
            data.pop(field)

            with pytest.raises(ValidationError):
                TransactionCreateSchema(**data)

        @pytest.mark.parametrize(
                'field, invalid_data',
                invalid,
                ids=lambda f: f"TransactionCreate_invalid_{f}"
        )
        def test_create_invalid(self, value, field, invalid_data):
            skip_test(field, ['id'])
            data = deepcopy(value)
            data[field] = invalid_data

            with pytest.raises(ValidationError):
                TransactionCreateSchema(**data)


@pytest.mark.parametrize('value', read_param)
class TestTransactionReadSchema:

    class TestValid:

        def test_read(self, value):
            TransactionReadSchema(**value)

    class TestInvalid:
        @pytest.mark.parametrize(
                'field',
                missing_fields,
                ids=lambda f: f'TransactionRead_missing_{f}'
        )
        def test_read_missing(self, value, field):
            skip_test(field, ['receiver_id', 'receiver_name'])
            data = deepcopy(value)
            data.pop(field)

            with pytest.raises(ValidationError):
                TransactionReadSchema(**data)

        @pytest.mark.parametrize(
                'field, invalid_data',
                invalid,
                ids=lambda f: f"TransactionRead_invalid_{f}"
        )
        def test_read_invalid(self, value, field, invalid_data):
            skip_test(field, ['receiver_id', 'receiver_name'])
            data = deepcopy(value)
            data[field] = invalid_data

            with pytest.raises(ValidationError):
                TransactionReadSchema(**data)


@pytest.mark.parametrize('value', update_param)
class TestTransactionUpdateSchema:

    class TestValid:
        def test_update(self, value):
            TransactionUpdateSchema(**value)

        @pytest.mark.parametrize(
                'field',
                missing_fields,
                ids=lambda f: f'TransactionUpdate_partial_missing_{f}'
        )
        def test_partial_update(self, value, field):
            skip_test(field, ['owner_id', 'receiver_name', 'receiver_id', 'id'])
            data = deepcopy(value)
            data.pop(field)

            TransactionUpdateSchema(**data)

    class TestInvalid:

        @pytest.mark.parametrize(
                'field, invalid_data',
                invalid,
                ids=lambda f: f"TransactionUpdate_invalid_{f}"
        )
        def test_update_invalid(self, value, field, invalid_data):
            skip_test(field, ['id', 'owner_id'])
            data = deepcopy(value)
            data[field] = invalid_data

            with pytest.raises(ValidationError):
                TransactionUpdateSchema(**data)


