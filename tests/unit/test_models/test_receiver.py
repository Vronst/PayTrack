import pytest
from sqlalchemy.exc import IntegrityError
from paytrack.models.receiver import Receiver


class TestPositiveReceiver:

    def test_creation(self, session):
        user_id: int = 1
        name: str = 'testname'
        receiver: Receiver = Receiver(owner_id=user_id, name=name)

        session.add(receiver)
        session.commit()

        assert receiver.name == name 
        assert receiver.owner_id == user_id


class TestNegativeReceiver:

    def test_creation_no_name(self, session):
        user_id: int = 1
        with pytest.raises(IntegrityError):
            receiver: Receiver = Receiver(owner_id=user_id)

            session.add(receiver)
            session.commit()

    def test_creation_no_owner_id(self, session):
        name: str = 'testname'
        with pytest.raises(IntegrityError):
            receiver: Receiver = Receiver(name=name)

            session.add(receiver)
            session.commit()

    def test_creation_nothing(self, session):
        with pytest.raises(IntegrityError):
            receiver: Receiver = Receiver()

            session.add(receiver)
            session.commit()

    def test_creation_too_long_name(self, session):
        name: str = 't' * 51
        user_id: int = 1
        with pytest.raises(ValueError):
            receiver: Receiver = Receiver(name=name, owner_id=user_id)

            session.add(receiver)
            session.commit()
