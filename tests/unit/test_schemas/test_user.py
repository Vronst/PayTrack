import pytest 
from pydantic import ValidationError 
from copy import deepcopy 

from paytrack.schemas import (
    UserCreateSchema,
    UserReadSchema,
    UserUpdateSchema,
)
from paytrack.constants.user import (
        NAME_LENGTH,
        PIN_LENGTH,
)
from .conftest import skip_test


create_params = [ 
        {
        'name': 'name',
        'surname': 'surname',
        'admin': True,
        'email': 'example@example.com',
        'phone': None,
        'premium': True,
        'parent_id': None,
        },
        {'name': 'company_name',
        'surname': None,
        'admin': False,
        'email': 'example2@example.com',
        'phone': '+48 999 999 999',
        'premium': False,
        'parent_id': 1,
         },
]

read_params = deepcopy(create_params)
for param in read_params:
    param['id'] = 1
    param['subaccounts'] = []
    param['included'] = []

update_params = deepcopy(create_params)
for param in update_params:
    param['pin'] = '1' * PIN_LENGTH
    param['password'] = 'p' * 8

missing_fields = [
        'id', 
        'name',
        'admin',
        'email',
        'premium',
]

invalid = [
        ('id', 'id'),
        ('name', 1),
        ('name', 'a' * NAME_LENGTH + 'a'),
        ('admin', 'admin'),
        ('email', 1),
        ('email', 'email'),
        ('email', 'email@email'),
        ('phone', 'a'),
        ('phone', '++999999999'),
        ('phone', '+999999999'),
        ('phone', '+48 999 999 9'),
        ('premium', 'invalid'),
        ('parent_id', 'id'),
]


@pytest.mark.parametrize('value', create_params)
class TestUserCreate:

    class TestValid:
        
        def test_create(self, value):
            UserCreateSchema(**value)

    class TestInvalid:

        @pytest.mark.parametrize(
                'field',
                missing_fields,
                ids=lambda f: f'UserCreate_missing_{f}'
        )
        def test_create_missing(self, value, field):
            skip_test(field, ['id', 'subaccounts', 'included'])
            data = deepcopy(value)
            data.pop(field)

            with pytest.raises(ValidationError):
                UserCreateSchema(**data)

        @pytest.mark.parametrize(
                'field, invalid_data',
                invalid,
                ids=lambda f: f'UserCreate_invalid_{f}'
        )
        def test_create_invalid(self, value, field, invalid_data):
            skip_test(field, ['id', 'subaccounts', 'included'])
            data = deepcopy(value)
            data[field] = invalid_data 

            with pytest.raises(ValidationError):
                UserCreateSchema(**data)


@pytest.mark.parametrize('value', read_params)
class TestUserRead:

    class TestValid:

        def test_read(self, value):
            UserReadSchema(**value)

    class TestInvalid:

        @pytest.mark.parametrize(
                'field',
                missing_fields,
                ids=lambda f: f'UserRead_missing_{f}'
        )
        def test_read_missing(self, value, field):
            data = deepcopy(value)
            data.pop(field)

            with pytest.raises(ValidationError):
                UserReadSchema(**data)

        @pytest.mark.parametrize(
                'field, invalid_data',
                invalid,
                ids=lambda f: f'UserRead_invalid_{f}'
        )
        def test_read_invalid(self, value, field, invalid_data):
            data = deepcopy(value)
            data[field] = invalid_data

            with pytest.raises(ValidationError):
                UserReadSchema(**data)


@pytest.mark.parametrize('value', update_params)
class TestUserUpdate:

    class TestValid:
        
        def test_update(self, value):
            UserUpdateSchema(**value)

        @pytest.mark.parametrize(
                'field',
                missing_fields,
                ids=lambda f: f'UserUpdate_partial_missing_{f}'
        )
        def test_partial_update_missing(self, value, field):
            skip_test(field, ['id'])
            data = deepcopy(value)
            data.pop(field)

            UserUpdateSchema(**data)

    class TestInvalid:

        @pytest.mark.parametrize(
                'field, invalid_data',
                invalid,
                ids=lambda f: f'UserUpdate_invalid_{f}'
        )
        def test_update_invalid(self, value, field, invalid_data):
            skip_test(field, ['id'])
            data = deepcopy(value)
            data[field] = invalid_data

            with pytest.raises(ValidationError):
                UserUpdateSchema(**data)

