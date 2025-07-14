from warnings import warn
from sqlalchemy import create_engine, Engine as EN
from sqlalchemy.orm import sessionmaker, scoped_session
import os
from ..models.base import Base


class Engine():
    """
            Creates, closes and manages:
            - engine (postgresql and sqlite for tests if other url is not provided)
            - session

            If arguments related to database are not provided,
            will look for environmental variables, named same but in uppercase.

            If some but not all database params are provided, will raise error.

            Args:
            test (bool): if True swaps targeted database to one provided in test_db arg.
            test_db_url (str): database url (for SQLAlchemy) that should be targeted during tests.
            user (str | None): database user, default None.
            password (str | None): password for database, default None.
            port (str | None): port for databse, default None.
            database (str | None): database to work with, default None.
            host (str | None): database host, default None.
    """
    engine: EN

    def __init__(
            self,
            *,
            test: bool = False, 
            test_db_url: str = 'sqlite:///:memory:',
            db_user: str | None = None, 
            db_password: str | None = None,
            port: str | None = None,
            database: str | None = None,
            host: str | None = None,            
    ):
        self._session = None
        self.test: bool = test or bool(os.getenv('TEST', False))

        if self.test:
            warn("Warning: Session is running on test database", RuntimeWarning)
            self.DB = test_db_url
        else:
            self.USER: str | None = db_user or os.getenv('DB_USER', None)
            self.PASSWORD: str | None = db_password or os.getenv('DB_PASSWORD', None)
            self.HOST: str | None = host or os.getenv('HOST', None)
            self.PORT: str | None = port or os.getenv('PORT', None)
            self.DATABASE: str | None = database or os.getenv('DATABASE', None) 

            if not all([
                self.USER,
                self.PASSWORD, 
                self.HOST,
                self.DATABASE,
                self.PORT]):
                variables: dict = {
                        "DB_USER": self.USER,
                        "DB_PASSWORD": self.PASSWORD,
                        "HOST": self.HOST,
                        "DATABASE": self.DATABASE,
                        "PORT": self.PORT
                }
                unset: list = [key for key, value in variables.items() if not value]
                raise ValueError(f'Following variables were not set: {unset}')
            else:
                self.DB: str = f'postgresql+psycopg://{self.USER}'\
                    f':{self.PASSWORD}@{self.HOST}:{self.PORT or 5432}/{self.DATABASE}'

    def create_session(self):
        """
        Creates engine and binds it to the session that is returned by this function.
        If session already exists, returns the existing session.

        Returns:
            scoped_session
        """
        if self._session:
            return self._session

        if not self.DB:
            raise ValueError('Engine has not been intialized properly')

        self.engine = create_engine(self.DB)
        local_session: sessionmaker = sessionmaker(bind=self.engine)
        # FIXME: scoped session is not needed
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
