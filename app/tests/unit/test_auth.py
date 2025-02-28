from ...auth import Authorization


class TestAuthorizationPositive:

    def test_empty_init(self, my_session) -> None:
        auth: Authorization = Authorization(engine=my_session)

        assert auth.user == None
        assert auth.guest == []
        assert auth.guest_list == []

    def test_register_init(self, my_session) -> None:
        auth: Authorization = Authorization(engine=my_session, action='register', username='registertestinit', password='Testpass!')

        assert auth.user != None
        assert auth.guest == []
        assert auth.guest_list == []

    def test_login_init(self, my_session) -> None:
        username: str = 'logintestinit'
        password: str = '1234'
        assert my_session.create_user(username=username, password=password) == True
        auth: Authorization = Authorization(engine=my_session, action='login', username=username, password=password)
        
        assert auth.user != None
        assert auth.user.name == username
        assert auth.guest == []
        assert auth.guest_list == []

    def test_logout(self, my_session) -> None:
        username: str = 'logouttest'
        password: str = '1234'
        assert my_session.create_user(username=username, password=password) == True
        auth: Authorization = Authorization(engine=my_session, action='login', username=username, password=password)
        
        assert auth.user != None
        assert auth.user.name == username
        auth.logout()
        assert auth.user == None

    def test_register(self, my_session) -> None:
        username: str = 'registertest'
        password: str = 'StrongPassword!'
        auth: Authorization = Authorization(engine=my_session)

        assert auth.register(username, password) == True
        assert auth.user != None
        assert auth.user.name == username

    def test_login(self, my_session) -> None:
        username: str = 'logintest'
        password: str = 'StrongPassword!'
        
        assert my_session.create_user(username, password) == True
        auth: Authorization = Authorization(engine=my_session)

        assert auth.login(username, password) == True
        assert auth.user != None
        assert auth.user.name == username


class TestAuthorizationNegative:

    def test_empty_init_no_engine(self) -> None:
        try:
            Authorization = Authorization()
        except UnboundLocalError:
            pass

    def test_reg_log_init_without_args(self, my_session) -> None:
        try:
            Authorization(engine=my_session, action='register')
        except TypeError:
            pass
        try:
             Authorization(engine=my_session, action='login')
        except TypeError:
            pass
        
    def test_register_init_user_exists(self, my_session) -> None:
        username: str = 'triue'
        password: str = 'StrongPassword!'
        my_session.create_user(username, password)

        try:
             Authorization(engine=my_session, action='register', username=username, password=password)
        except TypeError:
            pass

    def test_login_no_user_and_already_logged(self, my_session) -> None:
        username: str = 'tlnuaal'
        password: str = 'StrongPassword!'

        assert my_session.create_user(username, password) == True
        auth: Authorization = Authorization(engine=my_session, action='login', username='nouserlikethis', password='lol')
        assert auth.user == None
        assert auth.login(username, password) == True
        assert auth.user != None
        assert auth.user.name == username
        assert auth.login(username, password) == False

    def test_register_while_logged(self, my_session) -> None:
        username: str = 'tttrwl'
        password: str = 'StrongPassword!'
        assert my_session.create_user(username, password) == True
        auth: Authorization = Authorization(engine=my_session, action='login', username=username, password=password)
        assert auth.user != None
        assert auth.user.name == username
        assert auth.register(username='someotheruserhere', password=password) == False
         
