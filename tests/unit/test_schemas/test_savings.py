from copy import deepcopy
from datetime import datetime
from pydantic import ValidationError
import pytest
from .conftest import skip_test
from paytrack.schemas import SavingsCreateSchema, SavingsReadSchema, SavingsUpdateSchema

create_param = [{
        'amount': 11.5,
        'currency_id': 1,
        'owner_id': 1,
}]

read_param = deepcopy(create_param)
read_param[0]['id'] = 1
read_param[0]['included'] = []

update_param = deepcopy(create_param)

missing_fields = [ 
    'id',
    'owner_id',
    'currency_id',
    'amount',
    'included',
]

invalid_values = [
          ('id', 'id'),
          ('amount', 'amount'),
          ('currency_id', 'currency_id'),
          ('owner_id', 'owner_id'),
          ('budget', 'budget')
]


@pytest.mark.parametrize('value', create_param)
class TestSavingsCreate:

    class TestValid:
        def test_create(self, value):

            SavingsCreateSchema(**value)

        def test_create_with_budget(self, value):
            data = deepcopy(value)
            data['budget'] = 12.5

            SavingsCreateSchema(**data)

    class TestInvalid:
        
        @pytest.mark.parametrize(
            'field',
            missing_fields,
            ids=lambda f: f"SavingsCreate_missing_{f}",
        )
        def test_create_missing_field(self, value, field):
            skip_test(field, ['included', 'id'])
            data = deepcopy(value)
            data.pop(field)

            with pytest.raises(ValidationError):
                SavingsCreateSchema(**data)

        @pytest.mark.parametrize(
            'field, invalid_value',
            invalid_values,
            ids=lambda f: f"SavingsCreate_invalid_value_{f}",
        )
        def test_invalid_values(self, value, field, invalid_value):
            skip_test(field, ['id', 'included'])
            data = deepcopy(value)
            data[field] = invalid_value


@pytest.mark.parametrize('value', read_param)
class TestSavingsRead:

    class TestValid:
        def test_read(self, value):

            SavingsReadSchema(**value)

    class TestInvalid:
        @pytest.mark.parametrize(
            'field',
            missing_fields,
            ids=lambda f: f"SavingsRead_missing_{f}",
        )
        def test_missing_field(self, value, field):
            skip_test(field, ['included'])
            data = deepcopy(value)
            data.pop(field)

            with pytest.raises(ValidationError):
                SavingsReadSchema(**data)

        @pytest.mark.parametrize(
            'field, invalid_value',
            invalid_values,
            ids=lambda f: f"SavingsRead_invalid_value_{f}",
        )
        def test_invalid_values(self, value, field, invalid_value):
            data = deepcopy(value)
            data[field] = invalid_value

            with pytest.raises(ValidationError):
                SavingsReadSchema(**data)


@pytest.mark.parametrize('value', update_param)
class TestSavingsUpdate:

    class TestValid:

        def test_update(self, value):
            data = deepcopy(value)
            data['budget'] = 15.5

            result = SavingsUpdateSchema(**data)
            assert (result.updated_at - datetime.now()).total_seconds() < 5

        def test_partial_update(self, value):

            result = SavingsUpdateSchema(**value)
            assert (result.updated_at - datetime.now()).total_seconds() < 5


    class TestInvalid:

        @pytest.mark.parametrize(
            'field, invalid_value',
            invalid_values,
            ids=lambda f: f"SavingsUpdate_invalid_value_{f}",
        )

        def test_invalid_values(self, value, field, invalid_value):
            skip_test(field, ['id', 'owner_id'])
            data = deepcopy(value)
            data[field] = invalid_value

            with pytest.raises(ValidationError):
                SavingsUpdateSchema(**data)

