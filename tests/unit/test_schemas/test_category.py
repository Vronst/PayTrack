import pytest
from pydantic import ValidationError
from datetime import datetime
from paytrack.schemas import (
        CategoryUpdateSchema, 
        CategoryReadSchema,
        CategoryCreateSchema
)


class TestPositiveCategorySchema:

    def test_creation_custom(self):
        root_category: None = None 
        name: str = 'MyCategory'
        custom: bool = True

        CategoryCreateSchema(
            root_category=root_category,
            name=name,
            custom=custom
        )

    def test_creation(self):
        root_category: None = None 

        CategoryCreateSchema(
            root_category=root_category,
        )

    def test_update_extras(self):
        mock: dict = {
                'root_category': None,
                'name': 'my mock',
                'extra': 'extra'
        }

        result = CategoryUpdateSchema(**mock)

        assert result.updated_at.date() == datetime.now().date()

    def test_update(self):
        mock: dict = {
                'root_category': None,
                'name': 'my mock'
        }

        result = CategoryUpdateSchema(**mock)

        assert result.updated_at.date() == datetime.now().date()

    @pytest.mark.regression
    def test_partial_update(self):
        mock: dict = {
                'name': 'my mock'
        }

        result = CategoryUpdateSchema(**mock)

        assert result.updated_at.date() == datetime.now().date()

    def test_read(self):
        mock: dict = {
                'id': 1,
                'root_category': None,
        }

        result = CategoryReadSchema(**mock)
        assert result.subcategories == []

    def test_read_extras(self):
        mock: dict = {
                'id': 1,
                'root_category': None,
                'extra': 'extra'
        }

        result = CategoryReadSchema(**mock)
        assert result.subcategories == []

    def test_read_custom(self):
        mock: dict = {
                'id': 1,
                'root_category': None,
                'name': 'my mock',
                'custom': True
        }

        result = CategoryReadSchema(**mock)
        assert result.subcategories == []

    def test_read_custom_extras(self):
        mock: dict = {
                'id': 1,
                'root_category': None,
                'subcategories': [],
                'name': 'my mock',
                'extra': 'extra',
                'custom': True
        }

        result = CategoryReadSchema(**mock)
        assert result.subcategories == []

class TestNegativeCategorySchema:

    def test_creation_missing_name(self):
        root_category: None = None 
        custom: bool = True

        with pytest.raises(ValidationError):
            CategoryCreateSchema(
                root_category=root_category,
                custom=custom
            )

    @pytest.mark.regression
    def test_creation_name_non_custom(self):
        root_category: None = None 
        name: str = 'should not be here'

        with pytest.raises(ValidationError):
            CategoryCreateSchema(
                root_category=root_category,
                name=name
            )

    def test_read_root_as_list(self):
        data: dict = {
                'id': 1,
                'subcategories': [],
                'root_category': []
        }

        with pytest.raises(ValidationError):
            CategoryReadSchema(**data)

    def test_read_subcategories_as_None(self):
        data: dict = {
                'id': 1,
                'subcategories': None,
                'root_category': []
        }

        with pytest.raises(ValidationError):
            CategoryReadSchema(**data)

    def test_creation_custom_root_str(self):
        data: dict = {
                'root_category': 'root',
                'name': 'MyCategory',
                'custom': True,
        }

        with pytest.raises(ValidationError):
            CategoryCreateSchema(**data)

    def test_creation_custom_name_int(self):
        data: dict = {
                'root_category': 1,
                'name': 1,
                'custom': True,
        }

        with pytest.raises(ValidationError):
            CategoryCreateSchema(**data)

    def test_creation_custom_not_bool(self):
        data: dict = {
                'root_category': 1,
                'name': 1,
                'custom': 1,
        }

        with pytest.raises(ValidationError):
            CategoryCreateSchema(**data)

    def test_creation_root_str(self):
        data: dict = {
                'root_category': 'waht',
        }

        with pytest.raises(ValidationError):
            CategoryCreateSchema(**data)

    def test_creation_not_custom_not_bool(self):
        data: dict = {
                'root_category': 1,
                'custom': 'what'
        }

        with pytest.raises(ValidationError):
            CategoryCreateSchema(**data)

    def test_creation_not_custom_not_bool_with_name(self):
        data: dict = {
                'root_category': 1,
                'custom': 'what',
                'name': 'name'
        }

        with pytest.raises(ValidationError):
            CategoryCreateSchema(**data)

    def test_read_custom_id_str(self):
        mock: dict = {
                'id': 'not id',
                'root_category': None,
                'name': 'my mock',
                'custom': True
        }

        with pytest.raises(ValidationError):
            CategoryReadSchema(**mock)

    def test_read_custom_root_str(self):
        mock: dict = {
                'id': 1,
                'root_category': 'not ideal',
                'name': 'my mock',
                'custom': True
        }

        with pytest.raises(ValidationError):
            CategoryReadSchema(**mock)

    def test_read_custom_name_int(self):
        mock: dict = {
                'id': 1,
                'root_category': None,
                'name': 1,
                'custom': True
        }

        with pytest.raises(ValidationError):
            CategoryReadSchema(**mock)

    def test_read_custom_custom_none(self):
        mock: dict = {
                'id': 1,
                'root_category': None,
                'name': 'name',
                'custom': None
        }

        with pytest.raises(ValidationError):
            CategoryReadSchema(**mock)

    def test_update_root_str(self):
        mock: dict = {
                'root_category': 'my id',
                'name': 'my mock'
        }

        with pytest.raises(ValidationError):
            CategoryUpdateSchema(**mock)

    def test_update_name_int(self):
        mock: dict = {
                'root_category': None,
                'name': 1
        }

        with pytest.raises(ValidationError):
            CategoryUpdateSchema(**mock)
