import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from paytrack.models import (
    User,
    Base,
)


@pytest.fixture(scope='function')
def session():
    engine = create_engine('sqlite:///:memory:', echo=True)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope='function')
def users():
    u1 = User(name="John", surname="Smith", email="john@example.com", password="pw")
    u2 = User(name="Jane", surname="Doe", email="jane@example.com", password="pw")
    u3 = User(name="Mark", surname="Twain", email="mark@example.com", password="pw")
    return u1, u2, u3

