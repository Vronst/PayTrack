from collections.abc import Generator  # noqa: D100

import pytest

from paytrack.core import Engine


@pytest.fixture(scope="module")
def test_engine() -> Generator[Engine, None, None]:  # noqa: D103
    engine: Engine = Engine(test=True)

    yield engine

    engine.close()


@pytest.fixture(scope="module")
def test_manual_close_engine() -> Engine:  # noqa: D103
    engine: Engine = Engine(test=True)

    return engine
