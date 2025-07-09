from pydantic import ValidationError
import pytest
from paytrack.schemas import LanguageCreateSchema, LanguageReadSchema, LanguageUpdateSchema


class TestPositiveLanguageSchema:
    
    def test_create(self):
        data: dict = {
                'language_code': 'PL',
                'language_name': 'Polski'
        }

        LanguageCreateSchema(**data)

    def test_read(self):
        data: dict = {
                'language_code': 'PL',
                'language_name': 'Polski',
                'id': 1
        }

        LanguageReadSchema(**data)

    def test_update(self):
        data: dict = {
                'language_code': 'PL',
                'language_name': 'Polski'
        }

        LanguageUpdateSchema(**data)

    def test_partial_update(self):
        data: dict = {
                'language_name': 'Polski'
        }

        LanguageUpdateSchema(**data)


class TestNegativeLanguageSchema:

    def test_creation_missing_code(self):
        data: dict = {
                'language_name': 'Polski'
        }

        with pytest.raises(ValidationError):
            LanguageCreateSchema(**data)

    def test_creation_missing_name(self):
        data: dict = {
                'language_code': 'PL',
        }

        with pytest.raises(ValidationError):
            LanguageCreateSchema(**data)

    def test_read_missing_id(self):
        data: dict = {
                'language_code': 'PL',
                'language_name': 'Polski'
        }

        with pytest.raises(ValidationError):
            LanguageReadSchema(**data)

    def test_create_name_int(self):
        data: dict = {
                'language_code': 'PL',
                'language_name': 11
        }
        
        with pytest.raises(ValidationError):
            LanguageCreateSchema(**data)

    def test_create_code_int(self):
        data: dict = {
                'language_code': 11,
                'language_name': 'name'
        }

        with pytest.raises(ValidationError):
            LanguageCreateSchema(**data)

    def test_read_wrong_type_id(self):
        data: dict = {
                'language_code': 'PL',
                'language_name': 'Polski',
                'id': 'not int'
        }

        with pytest.raises(ValidationError):
            LanguageReadSchema(**data)

    def test_update_code_int(self):
        data: dict = {
                'language_code': 11,
                'language_name': 'Polski'
        }

        with pytest.raises(ValidationError):
            LanguageUpdateSchema(**data)
        
    def test_update_name_int(self):
        data: dict = {
                'language_code': 'PL',
                'language_name': 11
        }
        
        with pytest.raises(ValidationError):
            LanguageUpdateSchema(**data)
