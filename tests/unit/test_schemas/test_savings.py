from pydantic import ValidationError
import pytest
from paytrack.schemas import SavingsCreateSchema, SavingsReadSchema, SavingsUpdateSchema

# FIXME: fix this and DRY tests files above

class TestSavingsCreate:

    class TestValid:
        def test_create(self):
            data: dict = {
                    'amount': 11.5,
                    'currency_id': 1,
                    'owner_id': 1,
            }

            SavingsCreateSchema(**data)

        def test_create_with_budget(self):
            data: dict = {
                    'amount': 11.5,
                    'currency_id': 1,
                    'budget': 12.5,
                    'owner_id': 1,
            }

            SavingsCreateSchema(**data)

    class TestInvalid:



class TestPositiveSavingsSchema:

    def test_read(self):
        data: dict = {
                'id': 1,
                'amount': 11.5,
                'currency_id': 1,
                'owner_id': 1,
                'included': []
        }

        SavingsReadSchema(**data)

    def test_update(self):
        data: dict = {
                'amount': 11.5,
                'currency_id': 1,
                'owner_id': 1,
                'included': []
        }

        SavingsUpdateSchema(**data)

    def test_partial_update(self):
        data: dict = {
                'amount': 11.5,
                'included': []
        }

        SavingsUpdateSchema(**data)


class TestNegativeSavingsSchema:
    
    def test_create_missing_owner(self):
        data: dict = {
                'amount': 11.5,
                'currency_id': 1,
                'budget': 12.5,
        }

        with pytest.raises(ValidationError):
            SavingsCreateSchema(**data)

    def test_create_amount_str(self):
        data: dict = {
                'amount': 'amount',
                'currency_id': 1,
                'budget': 12.5,
                'owner_id': 1,
        }

        with pytest.raises(ValidationError):
            SavingsCreateSchema(**data)
        

    def test_create_currency_id_str(self):
        data: dict = {
                'amount': 11.5,
                'currency_id': 'id',
                'budget': 12.5,
                'owner_id': 1,
        }

        with pytest.raises(ValidationError):
            SavingsCreateSchema(**data)
        

    def test_create_budget_str(self):
        data: dict = {
                'amount': 11.5,
                'currency_id': 1,
                'budget': 'no',
                'owner_id': 1,
        }

        with pytest.raises(ValidationError):
            SavingsCreateSchema(**data)
        

    def test_create_owner_id_str(self):
        data: dict = {
                'amount': 11.5,
                'currency_id': 1,
                'budget': 12.5,
                'owner_id': 'uh',
        }

        with pytest.raises(ValidationError):
            SavingsCreateSchema(**data)
        

    def test_read_missing_id(self):
        data: dict = {
                'amount': 11.5,
                'currency_id': 1,
                'owner_id': 1,
                'included': []
        }

        with pytest.raises(ValidationError):
            SavingsReadSchema(**data)

    def test_read_amount_str(self):
        data: dict = {
                'id': 1,
                'amount': 'amount',
                'currency_id': 1,
                'owner_id': 1,
                'included': []
        }

        with pytest.raises(ValidationError):
            SavingsReadSchema(**data)

    def test_read_currency_str(self):
        data: dict = {
                'id': 1,
                'amount': 11.5,
                'currency_id': 'id',
                'owner_id': 1,
                'included': []
        }

        with pytest.raises(ValidationError):
            SavingsReadSchema(**data)

    def test_read_budget_str(self):
        data: dict = {
                'id': 1,
                'amount': 11.5,
                'currency_id': 1,
                'budget': 'string',
                'owner_id': 1,
                'included': []
        }

        with pytest.raises(ValidationError):
            SavingsReadSchema(**data)

    def test_read_owner_id_str(self):
        data: dict = {
                'id': 1,
                'amount': 11.5,
                'currency_id': 1,
                'owner_id': 'id',
                'included': []
        }

        with pytest.raises(ValidationError):
            SavingsReadSchema(**data)

    def test_read_included_str(self):
        data: dict = {
                'id': 1,
                'amount': 11.5,
                'currency_id': 1,
                'owner_id': 1,
                'included': '[]'
        }

        with pytest.raises(ValidationError):
            SavingsReadSchema(**data)

    def test_update_amount_str(self):
        data: dict = {
                'amount': 'amount',
                'currency_id': 1,
                'owner_id': 1,
                'included': []
        }

        with pytest.raises(ValidationError):
            SavingsUpdateSchema(**data)

    def test_currency_id_str(self):
        data: dict = {
                'amount': 11.5,
                'currency_id': 'id',
                'owner_id': 1,
                'included': []
        }

        with pytest.raises(ValidationError):
            SavingsUpdateSchema(**data)

    def test_update_budget_str(self):
        data: dict = {
                'amount': 11.5,
                'currency_id': 1,
                'budget': 'string',
                'owner_id': 1,
                'included': []
        }

        with pytest.raises(ValidationError):
            SavingsUpdateSchema(**data)

    def test_update_included_str(self):
        data: dict = {
                'amount': 11.5,
                'currency_id': 1,
                'owner_id': 1,
                'included': '[]'
        }

        with pytest.raises(ValidationError):
            SavingsUpdateSchema(**data)
