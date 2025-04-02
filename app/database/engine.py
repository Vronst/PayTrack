import os
from . import Tax 
from werkzeug.security import generate_password_hash
from warnings import warn
from dotenv import load_dotenv
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, scoped_session
from ..utils import simple_logs, list_of_taxes, UserCreationError
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

    def change_password(self, user_id: int, new_password: str) -> None:
        user: User | None = self.session.get(User, user_id)
        if not user:
            raise KeyError("User does not exist")
        user.password = generate_password_hash(new_password, salt_length=24)
        self.session.add(user)
        self.session.commit()
        print("Password changed successfully")
        return

    def default_taxes(self, user: User, *, path_to_file: str | None = None) -> list[str]:
        taxes: list[str] = list_of_taxes(path_to_file=path_to_file)
        for tax in taxes:
            new_tax: Tax = Tax(
                    taxname=tax,
                    user_id=user.id
            )
            user.taxes.append(new_tax)
        self.session.commit()
        return taxes

    def create_user(self, username: str, password: str, *, hashpass: bool = True, admin: bool = False, with_taxes: bool = True) -> User | None:
        """
        Allows for creation of user with any password
        Arguments:
            - username: str -> username
            - password: str -> password
            - hashpass: bool -> defualt True, hashes password and stores that hash instead
                of plain passowrd
        """
        if self.get_user(username):
            raise UserCreationError('Username is taken')
        if hashpass:
            from werkzeug.security import generate_password_hash
            password = generate_password_hash(password, salt_length=24)
        user: User = User(
                name=username,
                password=password,
                admin=admin
        )
        self.session.add(user)
        self.session.commit()

        if with_taxes:
            self.default_taxes(user)
        return user

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
        
        user: None | User
        if username:
            user = self.session.query(User).filter_by(name=username).first()
        else:
            user = self.session.get(User, user_id)

        return user

    def delete_user(self, *, username: str | None = None, id_: int | None = None) -> None:
        warn('If possible you should be using Auth.delete_user instead of engine.delete_user')

        user: User | None
        if not id_:
            user = self.get_user(username=username)
        else:
            user = self.get_user(user_id=id_)
        if not user:
            raise ValueError('User not found')
                    
        self.session.delete(user)
        self.session.commit()
        print(f'User {username} has been deleted')

        return

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
    def session(self) -> scoped_session:
        if self._session == None:
            self.create_my_session()
            print("Session was created due to it's being called")
        if self._session:
            return self._session  
        else:
            raise RuntimeError("Session could not be created")
    
    def close_session(self) -> None:
        """
            Closes session and dispose of engine
        """

        self.session.rollback()
        self.session.remove()
        if self.test:
            with self.engine.begin() as conn:
                Base.metadata.drop_all(bind=conn)
                simple_logs('Tables dropped successfully', log_file=['logs.txt', 'db.log'])
        self.engine.dispose()
        simple_logs('Session removed successfully', log_file=['logs.txt', 'db.log'])

