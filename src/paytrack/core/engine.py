from warnings import warn
from sqlalchemy import create_engine, Engine as EN
from sqlalchemy.orm import sessionmaker, scoped_session
import os
from ..models.base import Base


class Engine():
    """
            Creates, closes and manages:
            - engine (either sqlite or postgres)
            - session

            Args:
            test (bool): if True swaps targeted database to one provided in test_db arg.
            test_db (str): database that should be targeted during tests
    """
    engine: EN

    def __init__(self, test: bool = False, test_db: str | None = None):
        self._session: scoped_session | None = None
        self.test = test
        self.POSTGRES_USER = os.getenv('POSTGRES_USER', None)
        self.POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', None)
        self.POSTGRES_HOST = os.getenv('POSTGRES_HOST', None)
        self.POSTGRES_PORT = os.getenv('POSTGRES_PORT', None)
        if self.test:
            warn("Warning: Session is running on test database", RuntimeWarning)
            self.DataBase = test_db if test_db else 'sqlite:///:memory:'
        else:
            self.DataBase = os.getenv('DataBase', None)

        if not all([
            self.POSTGRES_USER,
            self.POSTGRES_PASSWORD, 
            self.POSTGRES_HOST,
            self.DataBase,
            self.POSTGRES_PORT]):
            raise ValueError('One or more environment variables are not set')

    def create_session(self) -> scoped_session:
        """
        Creates engine and binds it to the session that is returned by this function.
        If session already exists, returns the existing session.

        Returns:
            scoped_session
        """
        if self._session:
            return self._session

        if not self.DataBase:
            raise ValueError('Missing env variable - POSTGRESS_DB')
        if self.test and 'sqlite' in self.DataBase:
            self.engine = create_engine(self.DataBase)
        else:
            self.engine = create_engine(
                f'postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}'
                    f'@{self.POSTGRES_HOST}:{self.POSTGRES_PORT or 5432}/{self.DataBase}')
        local_session: sessionmaker = sessionmaker(bind=self.engine)
        self._session = scoped_session(local_session)

        if self.test:
            with self.engine.begin() as conn:
                Base.metadata.drop_all(bind=conn)
                # TODO: log this

        with self.engine.begin() as conn:
            Base.metadata.create_all(bind=conn)

        # TODO: log this too

        return self._session

    @property
    def session(self) -> scoped_session:
        if self._session == None:
            self.create_session()
            # TODO: log creating session without using method
        if self._session:
            return self._session  
        else:
            raise RuntimeError("Session could not be created")
    
    def close_session(self) -> None:
        """
            Closes session and disposes of engine
        """

        self.session.rollback()
        self.session.remove()
        if self.test:
            with self.engine.begin() as conn:
                Base.metadata.drop_all(bind=conn)
                # TODO: log deletion of test database tables
        self.engine.dispose()
        # TODO: log dispossing of session and engine
