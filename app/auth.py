from werkzeug.security import generate_password_hash, check_password_hash
from .database import User, MyEngine


class Authorization:
    user: User | None
    guest: list[int]  # so you can share you taxes
    guest_list: list[int]
    
    def __init__(self, *, engine: MyEngine, action: str | None = None, test: bool = False, **kwargs):
        self.user = None
        self.guest = [] 
        self.guest_list = []
        self.test = test
        self.engine= engine
        if action:
            try:
                if not eval(f'self.{action}("{kwargs.get("username")}", "{kwargs.get("password")}")'):
                    raise TypeError("Action returned False")
            except TypeError as e:
                print(f'Authorization: chosen action could not be called {e}')

    def login(self, username: str, password: str) -> bool:
        if self.user:
            return False
        selected_user: User | None = self.engine.get_user(username=username)
        if not isinstance(selected_user, User):
            return False
        if check_password_hash(selected_user.password, password):
            self.user = selected_user
            return True
        else:
            return False

    def logout(self) -> bool:
        if self.user == None:
            return False
        self.user = None
        self.guest = []
        self.guest_list = []
        return True

    def register(self, username: str, password: str) -> bool:
        if self.user != None:
            print("Logout first")
            return False
        if self.engine.get_user(username):
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
        hashed_passwd: str = generate_password_hash(password, salt_length=24)
        user: User = User(
            name=username,
            password=hashed_passwd
        )
        self.engine.session.add(user)
        self.engine.session.commit()
        self.user = user
        return True

