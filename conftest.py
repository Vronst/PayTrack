from typing import Any, Generator, Iterable
import pytest

from .app.auth import Authorization
from .app.services import Services
from .app.database import MyEngine
from .app.database import User


@pytest.fixture(scope="class")
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
def dict_of(my_session, monkeypatch) -> Generator[dict[str, Any], None, None]:
    username: str = 'toic'
    password: str = 'StrongPass!'
    admin_name: str = 'admin'
    admin: User = my_session.create_user(username=admin_name, password=admin_name, admin=True)
    no_taxes: User = my_session.create_user(username=username+'1', password=password+'1', with_taxes=False)
    # if not my_session.session.query(User).filter_by(name=username).first():
    auth: Authorization = Authorization(engine=my_session, action='register', username=username, password=password)
    # else:
        # auth = Authorization(engine=my_session, action='login', username=username, password=password)
    services: Services = Services(auth=auth, engine=my_session)

    yield {
        'engine': my_session,
        'auth': auth,
        'services': services,
        'user': {'username': username, 'password': password},
        'user_no_taxes': {'username': username+'1', 'password': password+'1'},
        'admin': {'username': admin_name, 'password': admin_name},
    }

    inputs: Iterable = iter(['Y'] * 4)
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    del services
    auth.logout()
    auth.login(username=admin_name, password=admin_name)
    auth.delete_user(username)
    auth.delete_user(username+'1')
    auth.delete_user(admin_name)
    del auth

