from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import scoped_session
from .database import User
from .service import select_user


class Authorization:
    user: User | None
    guest: list[int]  # so you can share you taxes
    guest_list: list[int]
    
    def __init__(self, session: scoped_session, action: str | None = None, test: bool = False):
        self.user = None
        self.guest = [] 
        self.guest_list = []
        self.test = test
        self.session = session
        if action:
            try:
                eval(f'self.{action}()')
            except TypeError:
                print('Authorization: chosen action could not be called')

    def login(self, username: str, password: str) -> bool:
        selected_user: User | None = select_user(username, session=self.session)
        if not isinstance(selected_user, User):
            return False
        if check_password_hash(selected_user.password, password):
            self.user = selected_user
            return True
        else:
            return False

    def logout(self) -> bool:
        self.user = None
        self.guest = []
        self.guest_list = []
        return True

    def register(self, username: str, password: str) -> bool:
        if select_user(username, self.session):
            print('Error: Username is already taken')
            return False
        if len(password) < 8:
            print('Password to short')
            return False
        if not any([x in password for x in "!@#$%^&*()?{}[]"]):
            print('Password requires at least one special sign')
            return False
        hashed_passwd: str = generate_password_hash(password, salt_length=24)
        user: User = User(
            name=username,
            password=hashed_passwd
        )
        self.session.add(user)
        self.session.commit()

        return True
