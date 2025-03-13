import pytest
from ...utils import LoginError, NameTaken, PasswordNotSafe
from ...auth import Authorization
from ...database import User, MyEngine


class TestAuthorizationPositive:

    def test_empty_init(self, my_session) -> None:
        auth: Authorization = Authorization(engine=my_session)

        assert auth.is_logged == False
        assert auth.guest == []
        assert auth.guest_list == []

    def test_register_init(self, my_session) -> None:
        auth: Authorization = Authorization(engine=my_session, action='register', username='registertestinit', password='Testpass!')

        assert auth.is_logged == True
        assert auth.guest == []
        assert auth.guest_list == []
        assert auth.user.taxes != []

    def test_login_init(self, my_session) -> None:
        username: str = 'logintestinit'
        password: str = '1234'
        assert my_session.create_user(username=username, password=password) != None, 'creating user by engine'
        auth: Authorization = Authorization(engine=my_session, action='login', username=username, password=password)
        
        assert auth.is_logged == True, 'user logged in?'
        assert auth.user.name == username, 'checking username'
        assert auth.guest == [], 'checking guests'
        assert auth.guest_list == [], 'checking guests list'

    def test_logout(self, my_session) -> None:
        username: str = 'logouttest'
        password: str = '1234'
        assert my_session.create_user(username=username, password=password) != None
        auth: Authorization = Authorization(engine=my_session, action='login', username=username, password=password)
        
        assert auth.is_logged == True
        assert auth.user.name == username
        auth.logout()
        assert auth.is_logged == False

    def test_register(self, my_session) -> None:
        username: str = 'registertest'
        password: str = 'StrongPassword!'
        auth: Authorization = Authorization(engine=my_session)

        assert auth.register(username, password) != None
        assert auth.is_logged == True
        assert auth.user.name == username

    def test_login(self, my_session) -> None:
        username: str = 'logintest'
        password: str = 'StrongPassword!'
        
        assert my_session.create_user(username, password) != None
        auth: Authorization = Authorization(engine=my_session)
        auth.login(username, password)

        assert auth.is_logged == True
        assert auth.user.name == username


class TestAuthorizationNegative:
    
    def test_no_session_init(self, no_session) -> None:
        auth: Authorization = Authorization(engine=no_session)
        assert auth.engine.session != None

    def test_overwriting_atributes(self, my_session) -> None:
        auth: Authorization = Authorization(engine=my_session)

        with pytest.raises(AttributeError, match="This attribute cannot be changed directly"):
            auth.user = User(name='test', password='test')

        with pytest.raises(AttributeError, match="This attribute cannot be changed directly"):
            auth.engine = MyEngine()

    def test_empty_init_no_engine(self) -> None:
        with pytest.raises(TypeError, match=''):
             Authorization()

    def test_reg_log_init_without_args(self, my_session) -> None:
        with pytest.raises(PasswordNotSafe, match='Password too short'):
            Authorization(engine=my_session, action='register')
        with pytest.raises(LoginError, match='User doesn\'t exists'):
             Authorization(engine=my_session, action='login')
        
    def test_register_init_user_exists(self, my_session) -> None:
        username: str = 'triue'
        password: str = 'StrongPassword!'
        my_session.create_user(username, password)

        with pytest.raises(NameTaken, match='Username is already taken'):
            Authorization(engine=my_session, action='register', username=username, password=password)

    def test_login_no_user_and_already_logged(self, my_session) -> None:
        username: str = 'tlnuaal'
        password: str = 'StrongPassword!'
        auth: Authorization | None = None

        assert my_session.create_user(username, password) != None
        with pytest.raises(LoginError, match='User doesn\'t exists'):
            auth = Authorization(engine=my_session, action='login', username='nouserlikethis', password='lol')
        if not auth:
            auth = Authorization(engine=my_session)
        assert auth.is_logged == False

        auth.login(username, password)

        assert auth.is_logged == True
        assert auth.user.name == username
        with pytest.raises(LoginError):
            auth.login(username, password)

    def test_register_while_logged(self, my_session) -> None:
        username: str = 'tttrwl'
        password: str = 'StrongPassword!'
        assert my_session.create_user(username, password) != None
        auth: Authorization = Authorization(engine=my_session, action='login', username=username, password=password)
        assert auth.is_logged == True
        assert auth.user.name == username
        assert auth.register(username='someotheruserhere', password=password) == False
         
