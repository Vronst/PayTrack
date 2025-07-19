from collections.abc import Generator  # noqa: D100

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from paytrack.models import Base, User


@pytest.fixture(scope="function")
def session() -> Generator[Session, None, None]:  # noqa: D103
    engine = create_engine("sqlite:///:memory:", echo=False)

    Base.metadata.create_all(bind=engine)

    LocalSession = sessionmaker(bind=engine)
    session = LocalSession()

    yield session

    session.close()

    Base.metadata.drop_all(bind=engine)

    engine.dispose()


@pytest.fixture(scope="function")
def users() -> tuple[User, User, User]:  # noqa: D103
    u1 = User(
        name="John", surname="Smith", email="john@example.com", password="pw"
    )
    u2 = User(
        name="Jane", surname="Doe", email="jane@example.com", password="pw"
    )
    u3 = User(
        name="Mark", surname="Twain", email="mark@example.com", password="pw"
    )

    return u1, u2, u3
