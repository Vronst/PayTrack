from typing import Any, Generator, Iterable
import pytest
from unittest.mock import MagicMock

from .app.database.models import User, Tax
from .app.auth import Authorization
from .app.services import Services
from .app.database import MyEngine
from .app.core import TextApp


@pytest.fixture(scope='function')
def app() -> TextApp:
    app: TextApp = TextApp()
    # my_session.create_user(username='test', password='test')
    return app

@pytest.fixture(scope='session')
def admin_user() -> User:
    return User(name='admin', password='admin', admin=True)

@pytest.fixture(scope='function')
def normal_user(my_session) -> User:
    user: User | None = my_session.create_user(
            username='selfstandinguser',
            password='mockpass',
            with_taxes=True
    )
    assert user is not None
    assert 'water' in [tax.taxname for tax in user.taxes if tax.taxname == 'water']
    return user


@pytest.fixture(scope='function')
def simple_user(my_session) -> User:
    user: User | None = my_session.create_user(
            username='selfstandinguser',
            password='mockpass',
            with_taxes=False
    )
    assert user is not None
    assert 'water' not in [tax.taxname for tax in user.taxes if tax.taxname == 'water']
    return user


@pytest.fixture(scope='function')
def mock_engine() -> MagicMock:
    user: User = User(name='examplemock', password='pass')
    user.taxes = [Tax(taxname='water')]
    universal_object = MagicMock()
    universal_object.price = 110
    universal_object.id = 1
    universal_object.name = 'examplemock'
    universal_object.date = '2023-10-11'
    universal_object.taxname = 'water'
    universal_object.taxes = [Tax(taxname='water')]
    engine = MagicMock()
    called_create_user: bool = False


    def mock_get_user(*args, **kwargs):
        nonlocal called_create_user
        if called_create_user:
            return user
        else:
            called_create_user = True
        return None

    def create_user_called(*args, **kwargs):
        nonlocal called_create_user
        called_create_user = True
        return user
    engine.get_user.side_effect = mock_get_user
    engine.create_user.side_effect = create_user_called
    engine.delete_user.return_value = None
    engine.session.query.return_value.filter_by.return_value.first.return_value = universal_object
    engine.session.query.return_value.filter_by.return_value.first.return_value.id = 1

    return engine


@pytest.fixture(scope='function')
def mock_engine_no_query() -> MagicMock:
    user: User = User(name='examplemock', password='pass')
    user.taxes = [Tax(taxname='water')]
    engine = MagicMock()
    called_create_user: bool = False

    def mock_get_user(*args, **kwargs):
        nonlocal called_create_user
        if called_create_user:
            return user
        else:
            called_create_user = True
        return None

    def create_user_called(*args, **kwargs):
        nonlocal called_create_user
        called_create_user = True
        return user
    engine.get_user.side_effect = mock_get_user
    engine.create_user.side_effect = create_user_called
    engine.delete_user.return_value = None
    engine.session.get.return_value = None
    engine.session.query.return_value.filter_by.return_value.first.return_value = None

    return engine

@pytest.fixture(scope='function')
def mock_engine_with_user() -> MagicMock:
    user: User = User(name='examplemock', password='pass')
    user.taxes = [Tax(taxname='testtax')]
    engine = MagicMock()
    engine.get_user.return_value = user
    engine.create_user.return_value = user
    engine.delete_user.return_value = None

    return engine


@pytest.fixture(scope='function')
def auth_mock_no_user() -> MagicMock:
    auth: MagicMock = MagicMock()
    auth.user = None
    return auth

@pytest.fixture(scope='function')
def auth_mock(my_session) -> Generator[MagicMock, None, None]:
    auth: MagicMock = MagicMock()
    user: User | None = my_session.create_user(
            username='mockuservalue',
            password='mockpass',
            with_taxes=True
    )
    assert user is not None
    assert 'water' in [tax.taxname for tax in user.taxes if tax.taxname == 'water']
    auth.user = user
    yield auth

    my_session.delete_user(username='mockuservalue')


@pytest.fixture(scope='function')
def auth_mock_user_no_taxes(my_session) -> Generator[MagicMock, None, None]:
    auth: MagicMock = MagicMock()
    auth.user.return_value = my_session.create_user(
            username='mockuservalue',
            password='mockpass',
            with_taxes=False
    )
    yield auth

    my_session.delete_user(username='mockuservalue')


@pytest.fixture(scope="function")
def my_session() -> Generator[MyEngine, None, None]:

    meng: MyEngine = MyEngine(test=True, test_db='testtaxes')
    meng.create_my_session()

    yield meng

    meng.close_session()


@pytest.fixture(scope='function')
def no_session() -> Generator[MyEngine, None, None]:
    meng: MyEngine = MyEngine(test=True, test_db='testtaxes')

    yield meng


@pytest.fixture(scope='function')
def ex_user(my_session) -> Generator[list[str], None, None]:
    returned_list: list[str] = ['thisuserisreal', 'thisishispass']
    my_session.create_user(returned_list[0], returned_list[1])

    yield returned_list

    my_session.delete_user(username=returned_list[0])


@pytest.fixture(scope='function')
def dict_of(my_session) -> Generator[dict[str, Any], None, None]:
    username: str = 'toic'
    password: str = 'StrongPass!'
    admin_name: str = 'admin'
    my_session.create_user(username=admin_name, password=admin_name, admin=True)
    my_session.create_user(username=username+'1', password=password+'1', with_taxes=False)
    auth: Authorization = Authorization(engine=my_session, action='register', username=username, password=password)
    assert auth.user is not None
    services: Services = Services(
        user=auth.user,
        engine=my_session)

    yield {
        'engine': my_session,
        'auth': auth,
        'services': services,
        'user': {'username': username, 'password': password},
        'user_no_taxes': {'username': username+'1', 'password': password+'1'},
        'admin': {'username': admin_name, 'password': admin_name},
    }

    inputs: Iterable = iter(['Y'] * 4)

    del services
    auth.logout()
    auth.login(username=admin_name, password=admin_name)
    try:
        auth.delete_user(username, input_method=lambda _: next(inputs))
        auth.delete_user(username+'1', input_method=lambda _: next(inputs))
        auth.delete_user(admin_name, input_method=lambda _: next(inputs))
    except ValueError:
        pass
    del auth

