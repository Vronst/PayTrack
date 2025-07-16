import pytest
from sqlalchemy.orm import Session


class TestPositiveEngine:

    def test_database_variable(self, test_engine):
        database_url: str = "sqlite:///:memory:"

        assert test_engine._DB_URL == database_url

    def test_create_session(self, test_engine):
        session = next(test_engine.get_session())

        assert session is not None
        assert isinstance(session, Session)

    def test_close_session(self, test_manual_close_engine):
        test_manual_close_engine.close()

    def test_close_session_check_session(self, test_manual_close_engine):
        test_manual_close_engine.close()

        with pytest.raises(RuntimeError):
            next(test_manual_close_engine.get_session())
