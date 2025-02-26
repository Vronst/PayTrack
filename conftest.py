from typing import Generator
import pytest
from sqlalchemy.orm import scoped_session


@pytest.fixture(scope="session")
def my_session() -> Generator[scoped_session, None, None]:
    from .app.database.engine import MyEngine

    meng: MyEngine = MyEngine(test=True, test_db='testtaxes')
    session: scoped_session = meng.create_my_session()

    yield session

    meng.close_session()

