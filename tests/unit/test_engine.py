import os
from sqlalchemy.orm import Session, scoped_session
from paytrack.core.engine import Engine


class TestPositiveEngine:

    def setup_method(self) -> None:
        os.environ["POSTGRES_USER"] = 'testuser'
        os.environ['POSTGRES_PASSWORD'] = 'testpass'
        os.environ['POSTGRES_HOST'] = 'localhost'
        os.environ['POSTGRES_PORT'] = '5432'
        os.environ['DataBase'] = 'test_db'

        self.engine = Engine(test=True, test_db='sqlite:///:memory:')

    def test_database_variable(self):
        database: str = 'sqlite:///:memory:'

        assert self.engine.DataBase == database
        new_engine = Engine(test=True)
        assert new_engine.DataBase == database

    def test_create_session(self):
        session = self.engine.create_session()

        assert session is not None 
        assert isinstance(session(), Session)

    def test_session_property(self):
        assert isinstance(self.engine.session(), Session)

    def test_close_session(self):
        self.engine.create_session()
        assert isinstance(self.engine.session, scoped_session)
        self.engine.close_session()

    def test_close_session_check_session(self):
        session = self.engine.create_session()()
        self.engine.close_session()
        session_after = self.engine.create_session()()
        assert session is not session_after


