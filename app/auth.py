from typing import Callable
from werkzeug.security import check_password_hash
from . import User, MyEngine
from .services import Services
from .utils import NameTaken, PasswordNotSafe, LoginError


class Authorization:
    # TODO: Maybe create abstract class and move some futures there?
    _user: User | None
    _guest: list[int]  # so you can share you taxes
    _guest_list: list[int]
    services: None | Services
    
    def __init__(self, *, engine: MyEngine, action: str | None = None, **kwargs):
        self._user = None
        self._guest = [] 
        self._guest_list = []
        self._engine = engine
        self.services = None
        if not kwargs.get('test', False) and not isinstance(self._engine, MyEngine):
            raise AttributeError("Engine should be of type MyEngine")
        if action:
            eval(f'self.{action}("{kwargs.get("username")}", "{kwargs.get("password")}")')
    
    @property
    def engine(self) -> MyEngine:
        return self._engine

    @engine.setter
    def engine(self, value) -> None:
        raise AttributeError("This attribute cannot be changed directly")

    @property
    def is_logged(self) -> bool:
        return True if self._user else False

    @property
    def guest(self) -> list[int]:
        return self._guest

    @property
    def guest_list(self) -> list[int]:
        return self._guest_list

    @property
    def user(self) -> User | None:
        return self._user

    @user.setter
    def user(self, *args) -> None:
        raise AttributeError("This attribute cannot be changed directly")

    def login(self, username: str, password: str) -> None:
        if username == '' or password == '' or username is None or password is None:
            raise LoginError("Username and password cannot be empty")
        if self._user:
            raise LoginError("Already logged in")
        selected_user: User | None = self._engine.get_user(username=username)
        if not isinstance(selected_user, User):
            raise LoginError("User doesn't exists")
        if check_password_hash(selected_user.password, password):
            self._user = selected_user
            self.services = Services(auth=self, engine=self._engine)
            return
        else:
            raise LoginError("Incorrect credentials")

    def logout(self) -> bool:
        if self._user == None:
            return False
        self._user = None
        self._guest = []
        self._guest_list = []
        self.services = None
        return True

    def register(self, username: str, password: str) -> bool:

        if username in ('', 'test', 'admin', None, ' ') or any(x in username for x in '!@# $%^&*()+_}{":?><~`,./;\'[]-='):
            raise ValueError('Username cannot contain special signs')
        if self._user != None:
            print("Logout first")
            return False
        if self._engine.get_user(username):
            raise NameTaken("Username is already taken")
        if len(password) < 8:
            raise PasswordNotSafe("Password too short")
        if not any([x in password for x in "!@#$%^&*()?{}[]"]):
            raise PasswordNotSafe("Password should contain at least one special sign")
        if not any([char.isupper() for char in password]):
            raise PasswordNotSafe("Password should contain at least one capital letter")
        if not any([char.islower() for char in password]):
            raise PasswordNotSafe("Password should contain at least one lower letter")
        user: User | None = self._engine.create_user(username, password)
        self._user = user
        self.services = Services(auth=self, engine=self._engine)
        return True
    
    def delete_user(self, username: str, *, input_method: Callable = input) -> None:
        if self.user and self.user.admin != True:
            raise LoginError('You must be logged as administrator to delete someones account!')

        user: User | None = self._engine.get_user(username=username)
        if not user:
            raise ValueError('User not found')

        print()
        if input_method(
            f'Are you sure you want to delete {user.id=} {user.name=} accont? (Y/n): '
        ) != 'Y':
            print('Abandoned action')
            return
        if self.user and self.user.name == username:
            if input_method(f'Are you sure you want to delete your own account? (Y,n): ') != 'Y':
                print('Deleting your own account was cancelled')
                return
            else:
                self.logout()
        self._engine.session.delete(user)
        self._engine.session.commit()
        print(f'Account of {username} has been deleted')

