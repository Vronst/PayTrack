from werkzeug.security import check_password_hash
from .database import User, MyEngine


class Authorization:
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

    def login(self, username: str, password: str) -> bool:
        if self._user:
            return False
        selected_user: User | None = self._engine.get_user(username=username)
        if not isinstance(selected_user, User):
            return False
        if check_password_hash(selected_user.password, password):
            self._user = selected_user
            return True
        else:
            return False

    def logout(self) -> bool:
        if self._user == None:
            return False
        self._user = None
        self._guest = []
        self._guest_list = []
        return True

    def register(self, username: str, password: str) -> bool:
        if self._user != None:
            print("Logout first")
            return False
        if self._engine.get_user(username):
            print('Error: Username is already taken')
            return False
        if len(password) < 8:
            print('Password to short')
            return False
        if not any([x in password for x in "!@#$%^&*()?{}[]"]):
            print('Password requires at least one special sign')
            return False
        if not any([char.isupper() for char in password]):
            print('Password must have at least one capital letter')
            return False
        if not any([char.islower() for char in password]):
            print('Password must have at least one lower letter')
            return False
        user: User | None = self._engine.create_user(username, password)
        # hashed_passwd: str = generate_password_hash(password, salt_length=24)
        # user: User = User(
        #     name=username,
        #     password=hashed_passwd
        # )
        # self._engine.session.add(user)
        # self._engine.default_taxes(user)  # adding default taxes
        # self._engine.session.commit()
        self._user = user
        return True

