from typing import Generator
import pytest
from .app.database.engine import MyEngine


@pytest.fixture(scope="class")
def my_session() -> Generator[MyEngine, None, None]:

    meng: MyEngine = MyEngine(test=True, test_db='testtaxes')
    meng.create_my_session()

    yield meng

    meng.close_session()


@pytest.fixture(scope='function')
def no_session() -> Generator[MyEngine, None, None]:
    meng: MyEngine = MyEngine(test=True, test_db='testtaxes')

    yield meng

