from copy import deepcopy
import pytest 
from pydantic import ValidationError 

from paytrack.schemas import SettingCreateSchema, SettingReadSchema, SettingUpdateSchema
from paytrack.constants.setting import MODE_CHOICES

create_params = [{
        'mode': MODE_CHOICES[0],
        'language_id': 1,
        'owner_id': 1,
}]

read_params = deepcopy(create_params)
read_params[0]['id'] = 1

update_params = deepcopy(create_params)
update_params[0].pop('owner_id')

invalid_data = [ 
    ('mode', 10),
    ('language_id', 'str'),
    ('owner_id', 'id')
]

missing_fields = [ 
        'mode',
        'language_id', 
        'owner_id',
]


@pytest.mark.parametrize('value', create_params)
class TestSettingCreate:

    class TestValid:

        def test_create(self, value):

            SettingCreateSchema(**value)

    class TestInvalid:

        @pytest.mark.parametrize('field,data', 
                                 invalid_data, 
                                 ids=lambda f: f'SettingCreate_invalid_value_{f}')
        def test_create_invalid_data(self, value, data, field):
            if field == 'id':
                return 
            data = deepcopy(value)
            data[field] = data

            with pytest.raises(ValidationError):
                SettingCreateSchema(**data)

        @pytest.mark.parametrize('field', missing_fields, ids=lambda f: f'SettingCreate_missing_{f}')
        def test_create_missing(self, value, field):
            data = deepcopy(value)
            data.pop(field)

            with pytest.raises(ValidationError):
                SettingCreateSchema(**data)


@pytest.mark.parametrize('value', read_params)
class TestSettingRead:

    class TestValid:

        def test_read(self, value):
            
            SettingReadSchema(**value)

    class TestInvalid:

        @pytest.mark.parametrize('field,data', 
                                 invalid_data, 
                                 ids=lambda f: f'SettingRead_invalid_value_{f}')
        def test_create_invalid_data(self, value, data, field):
            data = deepcopy(value)
            data[field] = data

            with pytest.raises(ValidationError):
                SettingReadSchema(**data)

        @pytest.mark.parametrize('field', missing_fields, ids=lambda f: f'SettingRead_missing_{f}')
        def test_create_missing(self, value, field):
            data = deepcopy(value)
            data.pop(field)

            with pytest.raises(ValidationError):
                SettingReadSchema(**data)


@pytest.mark.parametrize('value', update_params)
class TestSettingUpdate:

    class TestValid:

        def test_update(self, value):
            
            SettingUpdateSchema(**value)

        def test_partial_update(self, value):
            data = deepcopy(value)
            data.pop('language_id')
            
            SettingUpdateSchema(**data)

    class TestInvalid:

        def test_update_invalid_mode(self, value):
            data = deepcopy(value)
            data['mode'] = 'invalid mode'
            
            with pytest.raises(ValidationError):
                SettingUpdateSchema(**data)

        def test_update_language_str(self, value):
            data = deepcopy(value)
            data['language_id'] = 'str'
            
            with pytest.raises(ValidationError):
                SettingUpdateSchema(**data)

