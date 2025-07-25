import pytest
from pydantic import ValidationError 
from copy import deepcopy 

from paytrack.schemas import ( 
        TranslationCreateSchema,
        TranslationReadSchema, 
        TranslationUpdateSchema,
)
from .conftest import skip_test 
from paytrack.constants.translation import WORD_LENGTH 


create_param = [ 
        { 
        'category_id': 1, 
        'language_id': 1,
        'word': 'a'*WORD_LENGTH,
        }
]

read_param = deepcopy(create_param)
read_param[0]['id'] = 1 

update_param = deepcopy(create_param)

missing_fields = [ 
        'category_id', 
        'id',
        'language_id', 
        'word', 
] 

invalid = [ 
        ('id', 'id'),
        ('language_id', 'id'),
        ('word', 'a'*WORD_LENGTH + 'a'),
]


@pytest.mark.parametrize('value', create_param)
class TestTranslationCreate:

    class TestValid:
        
        def test_create(self, value):
            TranslationCreateSchema(**value)

    class TestInvalid:
        
        @pytest.mark.parametrize(
            'field',
            missing_fields,
            ids=lambda f: f'TranslationCreate_missing_{f}'
        )
        def test_create_missing(self, value, field):
            skip_test(field, ['id'])
            data = deepcopy(value)
            data.pop(field)

            with pytest.raises(ValidationError):
                TranslationCreateSchema(**data)

        @pytest.mark.parametrize(
                'field, invalid_data',
                invalid,
                ids=lambda f: f'TranslationCreate_invalid_{f}'
        )
        def test_create_invalid(self, value, field, invalid_data):
            skip_test(field, ['id'])
            data = deepcopy(value)
            data[field] = invalid_data

            with pytest.raises(ValidationError):
                TranslationCreateSchema(**data)


@pytest.mark.parametrize('value', read_param)
class TestTranslationRead:

    class TestValid: 
        
        def test_read(self, value):
            TranslationReadSchema(**value)

    class TestInvalid: 
        
        @pytest.mark.parametrize(
                'field',
                missing_fields,
                ids=lambda f: f'TranslationRead_missing_{f}'
        )
        def test_read_missing(self, value, field):
            data = deepcopy(value)
            data.pop(field)

            with pytest.raises(ValidationError):
                TranslationReadSchema(**data)

        @pytest.mark.parametrize(
                'field, invalid_data',
                invalid,
                ids=lambda f: f'TranslationRead_invalid_{f}'
        )
        def test_read_invalid(self, value, field, invalid_data):
            data = deepcopy(value)
            data[field] = invalid_data 

            with pytest.raises(ValidationError):
                TranslationReadSchema(**data)


@pytest.mark.parametrize('value', update_param)
class TestTranslationUpdate:

    class TestValid:
        
        def test_update(self, value):
            TranslationUpdateSchema(**value)

        @pytest.mark.parametrize(
                'field',
                missing_fields,
                ids=lambda f: f'TranslationUpdate_partial_missing_{f}'
        )
        def test_partial_update(self, value, field):
            skip_test(field, ['id'])
            data = deepcopy(value)
            data.pop(field)

            TranslationUpdateSchema(**data)


    class TestInvalid:
        @pytest.mark.parametrize(
                'field, invalid_data',
                invalid,
                ids=lambda f: f'TranslationRead_invalid_{f}'
        )
        def test_update_invalid(self, value, field, invalid_data):
            skip_test(field, ['id'])
            data = deepcopy(value)
            data[field] = invalid_data 

            with pytest.raises(ValidationError):
                TranslationUpdateSchema(**data)

