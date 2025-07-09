from pydantic import ValidationError
import pytest
from paytrack.schemas import CurrencyCreateSchema, CurrencyReadSchema, CurrencyUpdateSchema 


class TestPositiveCurrencySchema:

    def test_creation(self):
        data: dict = {
                'code': 'PLN',
                'name': 'Złoty',
                'value': 12.5
        }

        CurrencyCreateSchema(**data)

    def test_creation_extras(self):
        data: dict = {
                'code': 'PLN',
                'name': 'Złoty',
                'value': 12.5,
                'some': 'extras'
        }

        CurrencyCreateSchema(**data)

    def test_update(self):
        data: dict = {
                'name': 'Złocisz',
                'code': 'ZŁC',
                'value': 999
        }

        CurrencyUpdateSchema(**data)

    def test_partial_update(self):
        data: dict = {
                'name': 'Złocisz',
        }

        CurrencyUpdateSchema(**data)

    def test_read(self):
        data: dict = {
                'id': 1,
                'code': 'PLN',
                'name': "złoty",
                'value': 1
        }

        CurrencyReadSchema(**data)


class TestNegativeCurrencySchema:

    def test_create_missing_code(self):
        data: dict = {
                'name': 'złoty',
                'value': 11
        }

        with pytest.raises(ValidationError):
            CurrencyCreateSchema(**data)

    def test_create_missing_name(self):
        data: dict = {
                'value': 11,
                'code': 'PLN'
        }

        with pytest.raises(ValidationError):
            CurrencyCreateSchema(**data)

    def test_create_missing_value(self):
        data: dict = {
                'name': 'złoty',
                'code': 'PLN'
        }

        with pytest.raises(ValidationError):
            CurrencyCreateSchema(**data)

    def test_read_missing_id(self):
        data: dict = {
                'code': 'PLN',
                'name': "złoty",
                'value': 1
        }

        with pytest.raises(ValidationError):
            CurrencyReadSchema(**data)
            
    def test_creation_code_int(self):
        data: dict = {
                'code': 11,
                'name': 'Złoty',
                'value': 12.5,
        }

        with pytest.raises(ValidationError):
            CurrencyCreateSchema(**data)

    def test_creation_name_int(self):
        data: dict = {
                'code': 'PLN',
                'name': 11,
                'value': 12.5,
        }

        with pytest.raises(ValidationError):
            CurrencyCreateSchema(**data)

    def test_creation_value_str(self):
        data: dict = {
                'code': 'PLN',
                'name': 'Złoty',
                'value': 'some value'
        }

        with pytest.raises(ValidationError):
            CurrencyCreateSchema(**data)

    def test_read_id_str(self):
        data: dict = {
                'id': 'id',
                'code': 'PLN',
                'name': "złoty",
                'value': 1
        }

        with pytest.raises(ValidationError):
            CurrencyReadSchema(**data)
            
    def test_read_code_int(self):
        data: dict = {
                'id': 1,
                'code': 1,
                'name': "złoty",
                'value': 1
        }

        with pytest.raises(ValidationError):
            CurrencyReadSchema(**data)

    def test_read_name_int(self):
        data: dict = {
                'id': 1,
                'code': 'PLN',
                'name': 1,
                'value': 1
        }

        with pytest.raises(ValidationError):
            CurrencyReadSchema(**data)

    def test_read_value_str(self):
        data: dict = {
                'id': 1,
                'code': 'PLN',
                'name': "złoty",
                'value': 'some value'
        }

        with pytest.raises(ValidationError):
            CurrencyReadSchema(**data)

    def test_update_name_int(self):
        data: dict = {
                'name': 1,
                'code': 'ZŁC',
                'value': 999
        }

        with pytest.raises(ValidationError):
            CurrencyUpdateSchema(**data)

    def test_update_code_int(self):
        data: dict = {
                'name': 'Złocisz',
                'code': 1,
                'value': 999
        }

        with pytest.raises(ValidationError):
            CurrencyUpdateSchema(**data)

    def test_update_value_str(self):
        data: dict = {
                'name': 'Złocisz',
                'code': 'ZŁC',
                'value': 'value'
        }

        with pytest.raises(ValidationError):
            CurrencyUpdateSchema(**data)
