from typing import Generator

import pytest

from paytrack.core import Engine


@pytest.fixture(scope="module")
def test_engine() -> Generator[Engine, None, None]:
    engine: Engine = Engine(test=True)

    yield engine

    engine.close()


@pytest.fixture(scope="module")
def test_manual_close_engine() -> Engine:
    engine: Engine = Engine(test=True)

    return engine
