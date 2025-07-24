"""This module contains Engine.

Engine is used to connect and communicate with database.
"""

import os
from collections.abc import Iterator
from warnings import warn

from sqlalchemy import Engine as EN
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from ..models.base import Base


class Engine:
    """SQLAlchemy's engine. Created to work with PostgreSql.

    Creates, closes and manages:
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
        """Engine.

        If test is True, ignores all args except test_db_url. Else
        all other arguments must not be None.

        Args:
            test (bool): if true, uses test_db_url to connect to database.
            Ignores rest of args. Default False.

            test_db_url (str): Url passed to create_engine(). Default "sqlite:///:memory:"

            db_user (str | None): User used to log into database. Default None.

            db_password (str | None): Database user password. Default None.

            port (str | None): Port to connect to database. Default None.

            database (str | None): Name of database to connect to.
            Default None.

            host (str | None): Name of host. Default None.
        """
        self.active: bool = True
        self._test: bool = test or os.getenv("TEST", False) in ["True", "1"]

        if self._test:
            warn(
                "Warning: Session is running on test database",
                RuntimeWarning,
                stacklevel=2,
            )
            self._DB_URL = test_db_url
        else:
            self._USER: str | None = self.__get_env_or_default(db_user, "USER")
            self._PASSWORD: str | None = self.__get_env_or_default(
                db_password, "DB_PASSWORD"
            )
            self._HOST: str | None = self.__get_env_or_default(host, "HOST")
            self._PORT: str | None = self.__get_env_or_default(port, "PORT")
            self._DATABASE: str | None = self.__get_env_or_default(
                database, "DATABASE"
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

    def __get_env_or_default(
        self, value: str | None, env_var: str
    ) -> str | None:
        return value or os.getenv(env_var)

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

    # TODO: maybe add @contextmanager
    def get_session(self) -> Iterator[Session]:
        """Returns Session Iterator."""
        if not self.active:
            raise RuntimeError(
                "Cannot create session after enngine was closed"
            )

        session = self._session_maker()
        try:
            yield session
        finally:
            session.close()

    def close(self) -> None:
        """Closes session and disposes of engine."""
        self.active = False

        if self._test:
            self.__drop_models()

        self._engine.dispose()
        # TODO: log dispossing of session and engine
