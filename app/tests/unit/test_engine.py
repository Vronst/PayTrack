import pytest
from ...database import User
from ...utils import UserCreationError
from ...auth import Authorization 


class TestEnginePositive:
    @pytest.mark.regression
    def test_change_password(self, dict_of, capsys) -> None:
        user: User | None = dict_of['engine'].session.query(User).filter_by(
            name=dict_of['user']['username']
        ).first()
        assert user is not None
        new_password: str = 'new'
        dict_of['engine'].change_password(user_id=user.id, new_password=new_password)
        cap_output: str = capsys.readouterr().out.strip()
        assert 'Password changed successfully' in cap_output
        auth: Authorization = dict_of['auth']
        auth.logout()
        assert auth.user is None
        auth.login(username=user.name, password=new_password)
        assert auth.user is not None
        assert auth.user.name == user.name

    @pytest.mark.regression
    def test_create_session(self, no_session, capsys) -> None:
        assert no_session.session is not None
        captured_output: str = capsys.readouterr().out.strip()
        assert 'Session was created due to it\'s being called' in captured_output
        no_session.close_session()
        captured_output = capsys.readouterr().out.strip()
        assert 'Tables dropped successfully' in captured_output
        assert 'Session removed successfully' in captured_output
        assert no_session.create_my_session() is not None
        captured_output = capsys.readouterr().out.strip()
        assert 'Tables created successfully' in captured_output
        assert 'Tables dropped before creating successfully' in captured_output


    @pytest.mark.regression
    def test_close_session(self, my_session, capsys) -> None:
        my_session.close_session()
        captured_output: str = capsys.readouterr().out.strip()
        assert 'Tables dropped successfully' in captured_output
        assert 'Session removed successfully' in captured_output
        # assert my_session.session is not None
        # captured_output = capsys.readouterr().out.strip()
        # assert 'Session was created due to it\'s being called' in captured_output

    def test_create_user_and_get_user(self, my_session) -> None:
        username: str = 'tcmsen'
        password: str = 'StrongPass!'
        user: User | None = my_session.create_user(username=username, password=password)
        found_user: User | None = my_session.get_user(username=username)
        assert user is not None
        assert found_user is not None
        assert user.name == found_user.name
        assert user.id == found_user.id
        assert user.admin == False

    @pytest.mark.regression
    def test_create_admin_user(self, my_session) -> None:
        username: str = 'newadmin'
        password: str = '1234'

        admin_user: User = my_session.create_user(username=username, password=password, admin=True)
        assert admin_user is not None
        assert admin_user.name == username
        assert admin_user.admin == True
        assert my_session.get_user(username) is not None

    @pytest.mark.regression
    def test_delete_user(self, my_session) -> None:
        username: str = 'tdutdu'
        password: str = 'somepass'

        assert my_session.create_user(username, password) is not None
        assert my_session.get_user(username=username) is not None
        my_session.delete_user(username=username)
        assert my_session.get_user(username=username) is None

    @pytest.mark.regression
    def test_delete_user_by_id(self, my_session) -> None:
        username: str = 'tdutdu'
        password: str = 'somepass'

        assert my_session.create_user(username, password) is not None
        assert (user := my_session.get_user(username=username)) is not None
        my_session.delete_user(id_=user.id)
        assert my_session.get_user(username=username) is None

    @pytest.mark.regression
    def test_hashing_password(self, my_session) -> None:
        username: str = 'tspenlu'
        password: str = 'pass'

        my_session.create_user(username, password, hashpass=True)
        assert my_session.get_user(username=username).password != password
        my_session.delete_user(username=username)
        my_session.create_user(username, password, hashpass=False)
        assert my_session.get_user(username=username).password == password

    @pytest.mark.regression
    def test_create_user_no_pass(self, my_session) -> None:
        username: str = 'tcunpo'
        password: str = ''
        
        assert my_session.create_user(username, password) is not None
        user: User | None = my_session.get_user(username=username)
        assert user is not None
        assert user.password != ''
        my_session.delete_user(username=username)
        assert my_session.get_user(username=username) is None
        my_session.create_user(username, password, hashpass=False)
        user = my_session.get_user(username=username)
        assert user is not None
        assert user.password == ''

    @pytest.mark.regression
    def test_default_taxes(self, dict_of) -> None:
        user: User | None = dict_of['engine'].get_user(username=dict_of['user']['username'])      
        taxes: list[str] = dict_of['engine'].default_taxes(user=user)
        assert isinstance(taxes, list)
        assert taxes == [
            'water',
            'electricity',
            'gas',
            'internet',
            'phone',
            'house_tax',
            'ac/oc',
            'trash',
            'nursery',
            'school',
        ]

    @pytest.mark.regression
    def test_default_taxes_with_file(self, dict_of) -> None:
        import os
        path = os.path.dirname(__file__)
        file_path = os.path.join(path, 'taxes_list.txt')
        user: User | None = dict_of['engine'].get_user(username=dict_of['user']['username'])
        taxes: list[str] = dict_of['engine'].default_taxes(
            user=user,
            path_to_file=file_path)
        assert isinstance(taxes, list)
        assert taxes == ['file_water', 'file_school', 'file_hospital']


class TestEngineNegative:
    @pytest.mark.regression
    def test_create_user_that_already_exists(self, my_session) -> None:
        username: str = 'tcutaeen'
        password: str = '1234'

        my_session.create_user(username, password)
        with pytest.raises(UserCreationError, match='Username is taken'):
            my_session.create_user(username, password+'1')

    @pytest.mark.regression
    def test_default_taxes_with_file_wrong_path(self, dict_of) -> None:
        user: User | None = dict_of['engine'].get_user(username=dict_of['user']['username'])
        taxes: list[str] = dict_of['engine'].default_taxes(
            user=user,
            path_to_file='that/is/no/path')
        assert isinstance(taxes, list)
        assert taxes == [
            'water',
            'electricity',
            'gas',
            'internet',
            'phone',
            'house_tax',
            'ac/oc',
            'trash',
            'nursery',
            'school',
        ]

    def test_delete_not_existing_user_by_id(self, dict_of) -> None:
        user_id: int = 0  # may cause errors in future
        admin: User | None = dict_of['engine'].get_user(username=dict_of['admin']['username'])
        assert admin is not None
        assert dict_of['engine'].get_user(user_id=user_id) is None
        with pytest.raises(ValueError, match='User not found'):
            dict_of['engine'].delete_user(id_=user_id)
        assert dict_of['engine'].get_user(user_id=user_id) is None
