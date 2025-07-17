import pytest  # noqa: D100


class TestPositiveUser:  # noqa: D101
    @pytest.mark.regression
    def test_included_relationship(self, session, users) -> None:  # noqa: D102
        u1, u2, u3 = users

        u1.included.extend([u2, u3])

        session.add_all([u1, u2, u3])
        session.commit()

        assert u2 in u1.included
        assert u3 in u1.included

        assert u1 in u2.included_in
        assert u1 in u3.included_in

        assert u2.included == []
        assert u3.included == []

    @pytest.mark.regression
    def test_parent_and_child(self, session, users) -> None:  # noqa: D102
        u1, u2, u3 = users

        session.add_all([u1, u2, u3])
        session.commit()
        assert u1.subaccounts == []
        u2.parent_id = u1.id
        session.add(u2)
        session.commit()
        assert u1.subaccounts == [u2]

        u3.parent_id = u2.id
        session.add(u3)
        session.commit()

        assert u1.parent == None
        assert len(u1.subaccounts) == 1
        assert u2.subaccounts == [u3]
        assert u3.parent == u2


class TestNegativeUser:  # noqa: D101
    pass
