import pytest
from typing import Iterable
from paytrack.app.utils import LoginError, NameTaken
from paytrack.app.auth import Authorization
from paytrack.app.database import User


class TestAuthorizationPositive:

    def test_empty_init(self, my_session) -> None:
        auth: Authorization = Authorization(engine=my_session)

        assert auth.is_logged == False
        assert auth.guest == []
        assert auth.guest_list == []

    
    def test_register_init(self, my_session) -> None:
        auth: Authorization = Authorization(engine=my_session, action='register', username='registertestinit', password='Testpass!')

        assert auth.is_logged == True
        assert auth.user is not None
        assert auth.guest == []
        assert auth.guest_list == []
        assert auth.user.taxes != []
        assert auth.user.name == 'registertestinit'

    def test_login_init(self, my_session) -> None:
        username: str = 'logintestinit'
        password: str = '1234'
        assert my_session.create_user(username=username, password=password) != None, 'creating user by engine'
        auth: Authorization = Authorization(engine=my_session, action='login', username=username, password=password)
        
        assert auth.is_logged == True, 'user logged in?'
        assert auth.user is not None
        assert auth.user.name == username, 'checking username'
        assert auth.guest == [], 'checking guests'
        assert auth.guest_list == [], 'checking guests list'

    @pytest.mark.regression
    def test_logout(self, my_session) -> None:
        username: str = 'logouttest'
        password: str = '1234'
        assert my_session.create_user(username=username, password=password) != None
        auth: Authorization = Authorization(engine=my_session, action='login', username=username, password=password)
        
        assert auth.is_logged == True
        assert auth.user is not None
        assert auth.user.name == username
        auth.logout()
        assert auth.is_logged == False

    def test_register(self, my_session) -> None:
        username: str = 'registertest'
        password: str = 'StrongPassword!'
        auth: Authorization = Authorization(engine=my_session)

        assert auth.register(username, password) != None
        assert auth.is_logged == True
        assert auth.user is not None
        assert auth.user.name == username

    @pytest.mark.regression
    def test_login(self, my_session) -> None:
        username: str = 'logintest'
        password: str = 'StrongPassword!'
        
        assert my_session.create_user(username, password) != None
        auth: Authorization = Authorization(engine=my_session)
        auth.login(username, password)

        assert auth.is_logged == True
        assert auth.user is not None
        assert auth.user.name == username

    @pytest.mark.regression
    def test_delete_user(self, dict_of, capsys) -> None:
        inputs: Iterable = iter(['Y'])
        user: User | None = dict_of['engine'].get_user(username=dict_of['user']['username'])
        admin: User | None = dict_of['engine'].get_user(username=dict_of['admin']['username'])
        assert user is not None
        assert admin is not None
        username: str = user.name
        dict_of['auth'].logout()
        dict_of['auth'].login(username=admin.name, password=admin.name)
        dict_of['auth'].delete_user(username=username, input_method=lambda _: next(inputs))
        captured_output: str = capsys.readouterr().out.strip()
        assert 'You must be logged as administrator to delete someones account!' not in captured_output
        assert 'User not found' not in captured_output
        assert 'Abandoned action' not in captured_output
        assert 'Account of ' in captured_output
        assert dict_of['engine'].get_user(username=username) is None
        

class TestAuthorizationNegative:
    
    def test_no_session_init(self, no_session) -> None:
        auth: Authorization = Authorization(engine=no_session)
        assert auth.engine.session != None

    def test_register_init_user_exists(self, my_session) -> None:
        username: str = 'triue'
        password: str = 'StrongPassword!'
        my_session.create_user(username, password)

        with pytest.raises(NameTaken, match='Username is already taken'):
            Authorization(engine=my_session, action='register', username=username, password=password)

    @pytest.mark.regression
    def test_login_no_user_and_already_logged(self, my_session) -> None:
        username: str = 'tlnuaal'
        password: str = 'StrongPassword!'
        auth: Authorization | None = None

        assert my_session.create_user(username, password) != None
        with pytest.raises(LoginError, match='User doesn\'t exist'):
            auth = Authorization(engine=my_session, action='login', username='nouserlikethis', password='lol')
        if not auth:
            auth = Authorization(engine=my_session)
        assert auth.is_logged == False

        auth.login(username, password)

        assert auth.is_logged == True
        assert auth.user is not None
        assert auth.user.name == username
        with pytest.raises(LoginError):
            auth.login(username, password)


    @pytest.mark.regression
    def test_register_while_logged(self, my_session) -> None:
        username: str = 'tttrwl'
        password: str = 'StrongPassword!'
        assert my_session.create_user(username, password) != None
        auth: Authorization = Authorization(engine=my_session, action='login', username=username, password=password)
        assert auth.is_logged == True
        assert auth.user is not None
        assert auth.user.name == username
        assert auth.register(username='someotheruserhere', password=password) == False
         
    @pytest.mark.regression
    def test_delete_not_existing_user(self, dict_of) -> None:
        inputs: Iterable = iter(['Y'])
        username: str = 'ThatUserDoesNotExists'
        admin: User | None = dict_of['engine'].get_user(username=dict_of['admin']['username'])
        assert admin is not None
        assert dict_of['engine'].get_user(username=username) is None
        dict_of['auth'].logout()
        dict_of['auth'].login(username=admin.name, password=admin.name)
        with pytest.raises(ValueError, match='User not found'):
            dict_of['auth'].delete_user(username=username, input_method=lambda _: next(inputs))
        assert dict_of['engine'].get_user(username=username) is None

