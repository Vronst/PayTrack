import pytest  # noqa: D100
from sqlalchemy.orm import Session


class TestPositiveEngine:  # noqa: D101
    def test_database_variable(self, test_engine):  # noqa: D102
        database_url: str = "sqlite:///:memory:"

        assert database_url == test_engine._DB_URL

    def test_create_session(self, test_engine):  # noqa: D102
        session = next(test_engine.get_session())

        assert session is not None
        assert isinstance(session, Session)

    def test_close_session(self, test_manual_close_engine):  # noqa: D102
        test_manual_close_engine.close()

    def test_close_session_check_session(self, test_manual_close_engine):  # noqa: D102
        test_manual_close_engine.close()

        with pytest.raises(RuntimeError):
            next(test_manual_close_engine.get_session())
