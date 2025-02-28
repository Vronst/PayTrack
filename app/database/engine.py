import os
import datetime
from datetime import date
from . import Tax 
from warnings import warn
from dotenv import load_dotenv
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, scoped_session
from ..utils import simple_logs, list_of_taxes
from .models import Base, User


load_dotenv()

class MyEngine:
    """
            Creates engine and returns session
            Can be used to manipulate users directly without limitation.
            For example when creating user there is no need to care about
            length of the password.

            Can be initiated with arguments:
            - test: bool -> if true swaps targeted database from one from .env to on provided 
            with test_db arguments
            - test_db: str -> database that should be targeted during tests
    """
    def __init__(self, test: bool = False, test_db: str = ''):
        self._session: scoped_session | None = None
        self.test = test
        self.POSTGRES_USER = os.getenv('POSTGRES_USER', None)
        self.POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', None)
        self.POSTGRES_HOST = os.getenv('POSTGRES_HOST', None)
        self.POSTGRES_PORT = os.getenv('POSTGRES_PORT', None)
        if self.test:
            warn("Warning: Session is running on test database", RuntimeWarning)
            self.POSTGRES_DB = test_db
        else:
            self.POSTGRES_DB = os.getenv('POSTGRES_DB', None)

        if not all([
            self.POSTGRES_USER,
            self.POSTGRES_PASSWORD, 
            self.POSTGRES_HOST,
            self.POSTGRES_DB,
            self.POSTGRES_PORT]):
            raise ValueError('One or more environment variables are not set')

    def is_session_running(self) -> bool:
        if not self._session:
            warn("Warning: First initialize session", UserWarning)
            return False
        return True

    def create_user(self, username: str, password: str, hashpass: bool = True) -> bool:
        """
        Allows for creation of user with any password, and even duplicated username
        Arguments:
            - username: str -> username
            - password: str -> password
            - hashpass: bool -> defualt True, hashes password and stores that hash instead
                of plain passowrd
        """
        if not self.is_session_running():
            return False

        # TODO: each created user should have list of taxes to pay

        if hashpass:
            from werkzeug.security import generate_password_hash
            password = generate_password_hash(password, salt_length=24)
        user: User = User(
                name=username,
                password=password)
        self._session.add(user)
        self._session.commit()

        taxes: list[str] = list_of_taxes()
        for tax in taxes:
            new_tax: Tax = Tax(
                    taxname=tax,
                    user_id=user.id
            )
            user.taxes.append(new_tax)
        self._session.commit()
        return True

    def get_user(self, username: str | None = None, user_id: int | None = None) -> User | None:
        """
        Returns user from databse by name or id 
        Arguments:
            - username: str -> if provided searches by name
            - user_id: int -> if provided searches by id
            if both are provided username is first considered
        Returns:
            User
        """
        if not self.is_session_running:
            return None
        
        user: None | User
        if username:
            user = self._session.query(User).filter_by(name=username).first()
        else:
            user = self._session.query(User).get(user_id)

        return user

    def create_my_session(self) -> scoped_session:
        """
            Creates engine and binds it to the session that
            is retuned by this function. The session is also stored in 
            variable in this class
        Returns: session: scoped_session
        """
        if not self.POSTGRES_DB:
            raise ValueError('Missing env variable - POSTGRESS_DB')
        self.engine: Engine = create_engine(
            f'postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}'
                f'@{self.POSTGRES_HOST}:{self.POSTGRES_PORT or 5432}/{self.POSTGRES_DB}')
        local_session: sessionmaker = sessionmaker(bind=self.engine)
        self._session = scoped_session(local_session)

        if self.test:
            with self.engine.begin() as conn:
                Base.metadata.drop_all(bind=conn)
            simple_logs('Tables dropped before creating successfully', log_file=['logs.txt', 'db.log'])

        with self.engine.begin() as conn:
            Base.metadata.create_all(bind=conn)

        simple_logs('Tables created successfully', log_file=['logs.txt', 'db.log'])

        return self._session

    @property
    def session(self) -> scoped_session | None:
        return self._session
    
    def close_session(self) -> None:
        """
            Closes session and dispose of engine
        """
        if not self.is_session_running():
            return

        self._session.rollback()
        self._session.remove()
        if self.test:
            with self.engine.begin() as conn:
                Base.metadata.drop_all(bind=conn)
                simple_logs('Tables dropped successfully', log_file=['logs.txt', 'db.log'])
        self.engine.dispose()
        simple_logs('Session removed successfully', log_file=['logs.txt', 'db.log'])

    def update(self) -> None:
        """
        Updates the database with the current date.
        So the payments from last months won't count
        this month's taxes as paid.
        """
        self.is_session_running()

        today: date = datetime.date.today()
        day: int
        month: int
        year: int
        
        def change_status(tax: Tax) -> None:
            tax.payment_status = False
            self._session.add(tax)
            self._session.commit()
            simple_logs(f'{tax.taxname} payment status changed ({today.month, today.year})', log_file=['taxes.log'])
        
        taxes: list[Tax] = self._session.query(Tax).filter_by(payment_status=True).all()
        for tax in taxes:
            if not tax.payments:
                change_status(tax)
                continue
            for payment in tax.payments:
                day, month, year = list(map(int, payment.date.split('-')))
                if (month < today.month and year <= today.year) or year < today.year:
                    change_status(tax)
                    continue

