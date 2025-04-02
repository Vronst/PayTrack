import pytest
from ...utils import LoginError, PasswordNotSafe
from ...auth import Authorization
from ...database import User, MyEngine


class TestAuthorizationPositive:

    def test_empty_init(self, mock_engine) -> None:
        auth: Authorization = Authorization(engine=mock_engine, test=True)

        assert auth.is_logged == False
        assert auth.guest == []
        assert auth.guest_list == []

    
    def test_register_init(self,mock_engine) -> None:
        auth: Authorization = Authorization(engine=mock_engine, test=True, action='register', username='registertestinit', password='Testpass!')

        assert auth.is_logged == True
        assert auth.user is not None
        assert auth.guest == []
        assert auth.guest_list == []
        assert auth.user.taxes != []

    def test_logout(self, mock_engine) -> None:
        username: str = 'logouttest'
        password: str = 'Stongpass!'
        auth: Authorization = Authorization(engine=mock_engine, test=True, action='register', username=username, password=password)
        
        assert auth.is_logged == True
        assert auth.user is not None
        auth.logout()
        assert auth.is_logged == False

    def test_register(self, mock_engine) -> None:
        username: str = 'registertest'
        password: str = 'StrongPassword!'
        auth: Authorization = Authorization(engine=mock_engine, test=True)

        assert auth.register(username, password) != None
        assert auth.is_logged == True
        assert auth.user is not None


class TestAuthorizationNegative:
    
    def test_overwriting_atributes(self, mock_engine) -> None:
        auth: Authorization = Authorization(engine=mock_engine, test=True)

        with pytest.raises(AttributeError, match="This attribute cannot be changed directly"):
            auth.user = User(name='test', password='test')

        with pytest.raises(AttributeError, match="This attribute cannot be changed directly"):
            auth.engine = MyEngine()

    def test_empty_init_no_engine(self) -> None:
        with pytest.raises(TypeError, match=''):
             Authorization()

    def test_reg_log_init_without_args(self, mock_engine) -> None:
        with pytest.raises(PasswordNotSafe, match='Password too short'):
            Authorization(engine=mock_engine, test=True, action='register')
        with pytest.raises(LoginError):
             Authorization(engine=mock_engine, test=True, action='login')
        
    def test_login_already_logged(self, mock_engine) -> None:
        username: str = 'tlnuaal'
        password: str = 'StrongPassword!'
        auth: Authorization | None = None

        if not auth:
            auth = Authorization(engine=mock_engine, action='register', test=True, username=username, password=password)
        assert auth.is_logged == True

        assert auth.user is not None
        with pytest.raises(LoginError):
            auth.login(username, password)


    def test_register_while_logged(self, mock_engine) -> None:
        username: str = 'tttrwl'
        password: str = 'StrongPassword!'
        auth: Authorization = Authorization(engine=mock_engine, test=True, action='register', username=username, password=password)
        assert auth.is_logged == True
        assert auth.user is not None
        assert auth.register(username='someotheruserhere', password=password) == False
         
