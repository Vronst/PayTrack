from copy import deepcopy
from datetime import datetime
import pytest 
from pydantic import ValidationError 

from paytrack.schemas import SubscriptionCreateSchema, SubscriptionReadSchema, SubscriptionUpdateSchema 
from paytrack.constants.subscription import PERIOD_CHOICES, MIN_AMOUNT


# pytestmark = pytest.mark.parametrize(
#         'field,value', [ 
#             ('name', 'name'),
#             ('amount', 12.5), 
#             ('currency_id', 1),
#             ('period', PERIOD_CHOICES[0]),
#             ('shared', False),
#             ('active', True),
#             ('date', datetime.now().date()),
#             ('owner_id', 1)
#     ]
# )
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


class TestSubsriptionCreate:
    class TestValid:

        @pytest.mark.parametrize('value', create_param)
        def test_create(self, value):
            SubscriptionCreateSchema(**value)

    class TestInvalid:

        @pytest.mark.parametrize('value', create_param)
        def test_create_missing_name(self, value):
            data = deepcopy(value)
            data.pop('name')

            with pytest.raises(ValidationError):
                SubscriptionCreateSchema(**data)

        @pytest.mark.parametrize('value', create_param)
        def test_create_missing_amount(self, value):
            data = deepcopy(value)
            data.pop('amount')

            with pytest.raises(ValidationError):
                SubscriptionCreateSchema(**data)

        @pytest.mark.parametrize('value', create_param)
        def test_create_missing_currency_id(self, value):
            data = deepcopy(value)
            data.pop('currency_id')

            with pytest.raises(ValidationError):
                SubscriptionCreateSchema(**data)

        @pytest.mark.parametrize('value', create_param)
        def test_create_missing_period(self, value):
            data = deepcopy(value)
            data.pop('period')

            with pytest.raises(ValidationError):
                SubscriptionCreateSchema(**data)

        @pytest.mark.parametrize('value', create_param)
        def test_create_missing_shared(self, value):
            data = deepcopy(value)
            data.pop('shared')

            with pytest.raises(ValidationError):
                SubscriptionCreateSchema(**data)

        @pytest.mark.parametrize('value', create_param)
        def test_create_missing_active(self, value):
            data = deepcopy(value)
            data.pop('active')

            with pytest.raises(ValidationError):
                SubscriptionCreateSchema(**data)

        @pytest.mark.parametrize('value', create_param)
        def test_create_missing_date(self, value):
            data = deepcopy(value)
            data.pop('date')

            with pytest.raises(ValidationError):
                SubscriptionCreateSchema(**data)

        @pytest.mark.parametrize('value', create_param)
        def test_create_missing_owner_id(self, value):
            data = deepcopy(value)
            data.pop('owner_id')

            with pytest.raises(ValidationError):
                SubscriptionCreateSchema(**data)

        @pytest.mark.parametrize('value', create_param)
        def test_create_amount_below_lower(self, value):
            data = deepcopy(value)
            data['amount'] = MIN_AMOUNT - .1

            with pytest.raises(ValidationError):
                SubscriptionCreateSchema(**data)

        @pytest.mark.parametrize('value', create_param)
        def test_create_invalid_period(self, value):
            data = deepcopy(value)
            data['period'] = 'custom'

            with pytest.raises(ValidationError):
                SubscriptionCreateSchema(**data)

        @pytest.mark.parametrize('value', create_param)
        def test_create_name_int(self, value):
            data = deepcopy(value)
            data['name'] = 1

            with pytest.raises(ValidationError):
                SubscriptionCreateSchema(**data)

        @pytest.mark.parametrize('value', create_param)
        def test_create_amount_str(self, value):
            data = deepcopy(value)
            data['amount'] = 'value'

            with pytest.raises(ValidationError):
                SubscriptionCreateSchema(**data)

        @pytest.mark.parametrize('value', create_param)
        def test_create_currency_id_str(self, value):
            data = deepcopy(value)
            data['currency_id'] = 'str'

            with pytest.raises(ValidationError):
                SubscriptionCreateSchema(**data)

        @pytest.mark.parametrize('value', create_param)
        def test_create_shared_str(self, value):
            data = deepcopy(value)
            data['shared'] = 'maybe'

            with pytest.raises(ValidationError):
                SubscriptionCreateSchema(**data)

        @pytest.mark.parametrize('value', create_param)
        def test_create_active_str(self, value):
            data = deepcopy(value)
            data['active'] = 'probably'

            with pytest.raises(ValidationError):
                SubscriptionCreateSchema(**data)

        @pytest.mark.parametrize('value', create_param)
        def test_create_date_str(self, value):
            data = deepcopy(value)
            data['date'] = 'date'

            with pytest.raises(ValidationError):
                SubscriptionCreateSchema(**data)

        @pytest.mark.parametrize('value', create_param)
        def test_create_owner_id_str(self, value):
            data = deepcopy(value)
            data['owner_id'] = 'id'

            with pytest.raises(ValidationError):
                SubscriptionCreateSchema(**data)


class TestSubscriptionRead:
    class TestValid:

        @pytest.mark.parametrize('value', read_param)
        def test_read(self, value):
            SubscriptionReadSchema(**value) 

    class TestInvalid:

        @pytest.mark.parametrize('value', read_param)
        def test_read_missing_name(self, value):
            data = deepcopy(value)
            data.pop('name')
            
            with pytest.raises(ValidationError):
                SubscriptionReadSchema(**data)

        @pytest.mark.parametrize('value', read_param)
        def test_read_missing_amount(self, value):
            data = deepcopy(value)
            data.pop('amount')
            
            with pytest.raises(ValidationError):
                SubscriptionReadSchema(**data)

        @pytest.mark.parametrize('value', read_param)
        def test_read_missing_currency_id(self, value):
            data = deepcopy(value)
            data.pop('currency_id')
            
            with pytest.raises(ValidationError):
                SubscriptionReadSchema(**data)

        @pytest.mark.parametrize('value', read_param)
        def test_read_missing_id(self, value):
            data = deepcopy(value)
            data.pop('id')
            
            with pytest.raises(ValidationError):
                SubscriptionReadSchema(**data)

        @pytest.mark.parametrize('value', read_param)
        def test_read_missing_period(self, value):
            data = deepcopy(value)
            data.pop('period')
            
            with pytest.raises(ValidationError):
                SubscriptionReadSchema(**data)

        @pytest.mark.parametrize('value', read_param)
        def test_read_missing_shared(self, value):
            data = deepcopy(value)
            data.pop('shared')
            
            with pytest.raises(ValidationError):
                SubscriptionReadSchema(**data)

        @pytest.mark.parametrize('value', read_param)
        def test_read_missing_active(self, value):
            data = deepcopy(value)
            data.pop('active')
            
            with pytest.raises(ValidationError):
                SubscriptionReadSchema(**data)

        @pytest.mark.parametrize('value', read_param)
        def test_read_missing_date(self, value):
            data = deepcopy(value)
            data.pop('date')
            
            with pytest.raises(ValidationError):
                SubscriptionReadSchema(**data)

        @pytest.mark.parametrize('value', read_param)
        def test_read_missing_owner_id(self, value):
            data = deepcopy(value)
            data.pop('owner_id')
            
            with pytest.raises(ValidationError):
                SubscriptionReadSchema(**data)

        @pytest.mark.parametrize('value', read_param)
        def test_read_name_int(self, value):
            data = deepcopy(value)
            data['name'] = 1
            
            with pytest.raises(ValidationError):
                SubscriptionReadSchema(**data)

        @pytest.mark.parametrize('value', read_param)
        def test_read_amount_str(self, value):
            data = deepcopy(value)
            data['amount'] = 'str'
            
            with pytest.raises(ValidationError):
                SubscriptionReadSchema(**data)

        @pytest.mark.parametrize('value', read_param)
        def test_read_currency_id_str(self, value):
            data = deepcopy(value)
            data['currency_id'] = 'str'
            
            with pytest.raises(ValidationError):
                SubscriptionReadSchema(**data)

        @pytest.mark.parametrize('value', read_param)
        def test_read_invalid_period(self, value):
            data = deepcopy(value)
            data['period'] = 'my period'

            with pytest.raises(ValidationError):
                SubscriptionReadSchema(**data)

        @pytest.mark.parametrize('value', read_param)
        def test_read_shared_str(self, value):
            data = deepcopy(value)
            data['shared'] = 'could be'
            
            with pytest.raises(ValidationError):
                SubscriptionReadSchema(**data)

        @pytest.mark.parametrize('value', read_param)
        def test_read_active_str(self, value):
            data = deepcopy(value)
            data['active'] = 'possum'
            
            with pytest.raises(ValidationError):
                SubscriptionReadSchema(**data)

        @pytest.mark.parametrize('value', read_param)
        def test_read_date_str(self, value):
            data = deepcopy(value)
            data['date'] = 'date'
            
            with pytest.raises(ValidationError):
                SubscriptionReadSchema(**data)

        @pytest.mark.parametrize('value', read_param)
        def test_read_owner_id_str(self, value):
            data = deepcopy(value)
            data['owner_id'] = 'str'
            
            with pytest.raises(ValidationError):
                SubscriptionReadSchema(**data)

class TestSubscriptionUpdate:

    class TestValid:
        pass

    class TestInvalid:
        pass
