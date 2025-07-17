import os
from collections.abc import Generator
from warnings import warn

from sqlalchemy import Engine as EN
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from ..models.base import Base


class Engine:
    """Creates, closes and manages:
    - engine (postgresql and sqlite for tests
    if other url is not provided)
    - session

    If arguments related to database are not provided,
    will look for environmental variables, named same but in uppercase.

    If some but not all database params are provided, will raise error.

    Args:
    test (bool): if True swaps targeted database
    to one provided in test_db arg.

    test_db_url (str): database url (for SQLAlchemy)
    that should be targeted during tests.

    user (str | None): database user, default None.

    password (str | None): password for database, default None.

    port (str | None): port for databse, default None.

    database (str | None): database to work with, default None.

    host (str | None): database host, default None.
    """

    def __init__(
        self,
        *,
        test: bool = False,
        test_db_url: str = "sqlite:///:memory:",
        db_user: str | None = None,
        db_password: str | None = None,
        port: str | None = None,
        database: str | None = None,
        host: str | None = None,
    ):
        self.active: bool = True
        self._test: bool = test or bool(os.getenv("TEST", False))

        if self._test:
            warn(
                "Warning: Session is running on test database",
                RuntimeWarning,
            )
            self._DB_URL = test_db_url
        else:
            self._USER: str | None = db_user or os.getenv("DB_USER", None)
            self._PASSWORD: str | None = db_password or os.getenv(
                "DB_PASSWORD", None
            )
            self._HOST: str | None = host or os.getenv("HOST", None)
            self._PORT: str | None = port or os.getenv("PORT", None)
            self._DATABASE: str | None = database or os.getenv(
                "DATABASE", None
            )

            if not all(
                [
                    self._USER,
                    self._PASSWORD,
                    self._HOST,
                    self._DATABASE,
                    self._PORT,
                ]
            ):
                unset: dict = {
                    "DB_USER": self._USER,
                    "DB_PASSWORD": self._PASSWORD,
                    "HOST": self._HOST,
                    "DATABASE": self._DATABASE,
                    "PORT": self._PORT,
                }

                raise ValueError(
                    f"Following variables were not set:"
                    f" {[key for key, value in unset.items() if not value]}"
                )
            else:
                self._DB_URL: str = (
                    f"postgresql+psycopg://{self._USER}:{self._PASSWORD}@"
                    f"{self._HOST}:{self._PORT or 5432}/{self._DATABASE}"
                )

        self._engine: EN = create_engine(self._DB_URL)
        self._session_maker = sessionmaker(bind=self._engine)
        self.__init_models()

    def __init_models(self) -> None:
        if self._test:
            with self._engine.begin() as conn:
                Base.metadata.drop_all(bind=conn)
                # TODO: log this
        with self._engine.begin() as conn:
            Base.metadata.create_all(bind=conn)
        # TODO: log this too

    def __drop_models(self) -> None:
        if self._test:
            with self._engine.begin() as conn:
                Base.metadata.drop_all(bind=conn)
                # TODO: log deletion of test database tables

    def get_session(self) -> Generator[Session, None, None]:
        if not self.active:
            raise RuntimeError("Cannot create session after enngine was close")

        session = self._session_maker()
        try:
            yield session
        finally:
            session.close()

    def close(self) -> None:
        """Closes session and disposes of engine"""
        self.active = False

        if self._test:
            self.__drop_models()

        self._engine.dispose()
        # TODO: log dispossing of session and engine
