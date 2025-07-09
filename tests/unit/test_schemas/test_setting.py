import pytest 
from pydantic import ValidationError 

from paytrack.schemas import SettingCreateSchema, SettingReadSchema, SettingUpdateSchema
from paytrack.constants.setting import MODE_CHOICES


class TestPositiveSettingSchema:
    
    def test_create(self):
        data: dict = {
                'mode': MODE_CHOICES[0],
                'language_id': 1,
                'owner_id': 1,
        }

        SettingCreateSchema(**data)

    def test_read(self):
        data: dict = {
                'id': 1,
                'mode': MODE_CHOICES[0],
                'language_id': 1,
                'owner_id': 1,
        }
        
        SettingReadSchema(**data)

    def test_update(self):
        data: dict = {
                'mode': MODE_CHOICES[0],
                'language_id': 1,
        }
        
        SettingUpdateSchema(**data)

    def test_partial_update(self):
        data: dict = {
                'language_id': 1,
        }
        
        SettingUpdateSchema(**data)


class TestNegativeSettingSchema:
    
    def test_create_missing_owner(self):
        data: dict = {
                'mode': MODE_CHOICES[0],
                'language_id': 1,
        }

        with pytest.raises(ValidationError):
            SettingCreateSchema(**data)

    def test_create_missing_language(self):
        data: dict = {
                'mode': MODE_CHOICES[0],
                'owner_id': 1,
        }

        with pytest.raises(ValidationError):
            SettingCreateSchema(**data)
        pass 

    def test_create_missing_mode(self):
        data: dict = {
                'language_id': 1,
                'owner_id': 1,
        }

        with pytest.raises(ValidationError):
            SettingCreateSchema(**data)
        
    def test_create_invalid_mode(self):
        data: dict = {
                'mode': 'my_mode',
                'language_id': 1,
                'owner_id': 1,
        }

        with pytest.raises(ValidationError):
            SettingCreateSchema(**data)

    def test_read_missing_id(self):
        data: dict = {
                'mode': MODE_CHOICES[0],
                'language_id': 1,
                'owner_id': 1,
        }
        
        with pytest.raises(ValidationError):
            SettingReadSchema(**data)

    def test_read_missing_mode(self):
        data: dict = {
                'id': 1,
                'language_id': 1,
                'owner_id': 1,
        }
        
        with pytest.raises(ValidationError):
            SettingReadSchema(**data)

    def test_read_invalid_mode(self):
        data: dict = {
                'id': 1,
                'mode': 'my_mode',
                'language_id': 1,
                'owner_id': 1,
        }
        
        with pytest.raises(ValidationError):
            SettingReadSchema(**data)

    def test_read_missing_language(self):
        data: dict = {
                'id': 1,
                'mode': MODE_CHOICES[0],
                'owner_id': 1,
        }
        
        with pytest.raises(ValidationError):
            SettingReadSchema(**data)

    def test_update_invalid_mode(self):
        data: dict = {
                'mode': 'mode',
                'language_id': 1,
        }
        
        with pytest.raises(ValidationError):
            SettingUpdateSchema(**data)

    def test_update_language_str(self):
        data: dict = {
                'mode': MODE_CHOICES[0],
                'language_id': 'id',
        }
        
        with pytest.raises(ValidationError):
            SettingUpdateSchema(**data)

