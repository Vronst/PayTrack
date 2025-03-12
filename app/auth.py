from werkzeug.security import check_password_hash
from .database import User, MyEngine
from .utils import NameTaken, PasswordNotSafe, LoginError


class Authorization:
    # TODO: Maybe create abstract class and move some futures there?
    _user: User | None
    _guest: list[int]  # so you can share you taxes
    _guest_list: list[int]
    
    def __init__(self, *, engine: MyEngine, action: str | None = None, **kwargs):
        self._user = None
        self._guest = [] 
        self._guest_list = []
        self._engine= engine
        if not isinstance(self._engine, MyEngine):
            raise AttributeError("Engine should be of type MyEngine")
        # if not self._engine.session and not no_init:
        #     print("To avoid errors, session has been started")
        #     self._engine.create_my_session()
        if action:
            if not eval(f'self.{action}("{kwargs.get("username")}", "{kwargs.get("password")}")'):
                raise TypeError("Action returned False")
    
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
        if username == '' or password == '':
            raise LoginError("Username and password cannot be empty")
        if self._user:
            raise LoginError("Already logged in")
        selected_user: User | None = self._engine.get_user(username=username)
        if not isinstance(selected_user, User):
            raise LoginError("User doesn't exists")
        if check_password_hash(selected_user.password, password):
            self._user = selected_user
            return
        else:
            raise LoginError("Incorrect credentials")

    def logout(self) -> bool:
        if self._user == None:
            return False
        self._user = None
        self._guest = []
        self._guest_list = []
        return True

    def register(self, username: str, password: str) -> bool:

        if username == '' or any(x in username for x in '!@#$%^&*()+_}{":?><~`,./;\'[]-='):
            # print('Illegal username')
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
        return True

