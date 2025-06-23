import pytest 
from paytrack.models import User


class TestPositiveUser:
    
    @pytest.mark.regression
    def test_included_relationship(self, session) -> None:
        u1 = User(name="John", surname="Smith", email="john@example.com", password="pw")
        u2 = User(name="Jane", surname="Doe", email="jane@example.com", password="pw")
        u3 = User(name="Mark", surname="Twain", email="mark@example.com", password="pw")

        u1.included.extend([u2, u3])

        session.add_all([u1, u2, u3])
        session.commit()

        assert u2 in u1.included
        assert u3 in u1.included

        assert u1 in u2.included_in
        assert u1 in u3.included_in

        assert u2.included == []


class TestNegativeUser:
    pass
