from pydantic import ValidationError
import pytest

from paytrack.schemas import ReceiverCreateSchema, ReceiverReadSchema, ReceiverUpdateSchema


class TestPositiveReceiverSchema:
    
    def test_create(self):
        data: dict = {
                'owner_id': 1,
                'name': 'name',
        }
        
        ReceiverCreateSchema(**data)
        
    def test_create_casting(self):
        data: dict = {
                'owner_id': '1',
                'name': 'name',
        }
        
        ReceiverCreateSchema(**data)

    def test_create_extras(self):
        data: dict = {
                'owner_id': 1,
                'name': 'name',
                'some': 'extras'
        }
        
        ReceiverCreateSchema(**data)

    def test_read_extras(self):
        data: dict = {
                'owner_id': 1,
                'name': 'name',
                'some': 'extras',
                'id': 1,
                'included': []
        }
        
        ReceiverReadSchema(**data)

    def test_read(self):
        data: dict = {
                'owner_id': 1,
                'name': 'name',
                'id': 1,
                'included': []
        }
        
        ReceiverReadSchema(**data)
    

    def test_update_extras(self):
        data: dict = {
                'name': 'name',
                'included': [],
                'some': 'extras'
        }
        
        ReceiverUpdateSchema(**data)

    def test_update(self):
        data: dict = {
                'name': 'name',
                'included': [],
        }
        
        ReceiverUpdateSchema(**data)

    def test_partial_update(self):
        data: dict = {
                'name': 'name',
        }
        
        ReceiverUpdateSchema(**data)


class TestNegativeReceiverSchema:

    def test_create_missing_owner(self):
        data: dict = {
                'name': 'name',
        }
        
        with pytest.raises(ValidationError):
            ReceiverCreateSchema(**data)

    def test_create_missing_name(self):
        data: dict = {
            'owner_id': 1
        }
        
        with pytest.raises(ValidationError):
            ReceiverCreateSchema(**data)

    def test_read_no_id(self):
        data: dict = {
                'owner_id': 1,
                'name': 'name',
                'included': []
        }
       
        with pytest.raises(ValidationError):
            ReceiverReadSchema(**data)

    def test_read_owner_id_str(self):
        data: dict = {
                'owner_id': 'should be int',
                'name': 'name',
                'included': []
        }
       
        with pytest.raises(ValidationError):
            ReceiverReadSchema(**data)

    def test_create_owner_id_str(self):
        data: dict = {
                'owner_id': 'should be int',
                'name': 'name',
        }
       
        with pytest.raises(ValidationError):
            ReceiverCreateSchema(**data)

    def test_update_name_int(self):
        data: dict = {
                'name': 11,
                'included': []
        }
       
        with pytest.raises(ValidationError):
            ReceiverUpdateSchema(**data)

    def test_update_included_str(self):
        data: dict = {
                'name': 'name',
                'included': '[]'
        }
       
        with pytest.raises(ValidationError):
            ReceiverUpdateSchema(**data)

