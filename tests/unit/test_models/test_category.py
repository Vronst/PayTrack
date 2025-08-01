import pytest  # noqa: D100

from paytrack.models.category import Category
from paytrack.services.date import utc_now


class TestPositiveCategory:  # noqa: D101
    @pytest.mark.regression
    def test_created_at(self, session):  # noqa: D102
        category: Category = Category()
        session.add(category)
        session.commit()

        now = utc_now()

        # assert category.created_at.day == now.day
        # assert category.created_at.month == now.month
        # assert category.created_at.year == now.year
        assert category.created_at.date() == now.date()
        assert category.translations == []

    @pytest.mark.regression
    def test_updated_at(self, session):  # noqa: D102
        category: Category = Category()
        session.add(category)
        session.commit()

        assert category.updated_at is None

        category.custom = True
        category.name = "new name"
        session.add(category)
        session.commit()

        assert category.updated_at is not None

    @pytest.mark.regression
    def test_deleted_at(self, session):  # noqa: D102
        category: Category = Category()
        session.add(category)
        session.commit()

        assert category.deleted_at is None

    def test_parent_and_subcategories(self, session):  # noqa: D102
        parent: Category = Category()
        child: Category = Category()
        grandparent: Category = Category()

        child.root = parent

        session.add_all([parent, child, grandparent])
        session.commit()

        assert grandparent.root_category is None
        assert grandparent.subcategories == []

        assert parent.subcategories == [child]
        assert parent.root is None

        assert child.root == parent
        assert child.subcategories == []

        grandparent.subcategories = [parent]
        session.add(grandparent)
        session.commit()

        assert parent.root == grandparent
        assert grandparent.subcategories == [parent]


class TestNegativeCategory:  # noqa: D101
    def test_too_long_name(self, session):  # noqa: D102
        name: str = "x" * 20
        with pytest.raises(ValueError):
            category: Category = Category(name=name)
            session.add(category)
            session.commit()

    def test_incorect_type(self, session):  # noqa: D102
        root_category: str = "Incorect type"
        category: Category = Category()

        with pytest.raises(ValueError):
            category.root_category = root_category
