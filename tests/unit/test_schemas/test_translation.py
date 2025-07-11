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
# FIXME: replace ... with tests


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
        ...

    class TestInvalid:
        ...


@pytest.mark.parametrize('value', read_param)
class TestTranslationRead:

    class TestValid: 
        ...

    class TestInvalid: 
        ...


@pytest.mark.parametrize('value', update_param)
class TestTranslationUpdate:

    class TestValid:
        ...

    class TestInvalid:
        ...

