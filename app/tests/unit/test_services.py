import pytest
from ...auth import Authorization
from ...services import Services
from ...database import MyEngine


class TestServicesPositive:

    def test_check_taxes(self, capsys, my_session):
        username: str = 'checktaxes'
        password: str = 'StrongPass!'
        auth: Authorization = Authorization(engine=my_session, action='register', username=username, password=password)
        assert auth.user != None
        services: Services = Services(auth, my_session)

        services.check_taxes(simple=True)
        captured_output = capsys.readouterr()
        assert 'water' in captured_output.out.strip()
    

class TestServicesNegative:
            
    def test_changing_unchangable_attributes(self, my_session) -> None:
        username: str = 'TCua'
        password: str = 'StrongPass!'
        auth: Authorization = Authorization(engine=my_session, action='register', username=username, password=password)
        services: Services = Services(auth=auth, engine=my_session)

        with pytest.raises(AttributeError, match='This attribute cannot be changed directly'):
            services.auth = Authorization(engine=MyEngine())

        with pytest.raises(AttributeError, match='This attribute cannot be changed directly'):
            services.engine = MyEngine()

    def test_check_taxes_not_logged_in(self, my_session) -> None:
        auth: Authorization = Authorization(engine=my_session)
        with pytest.raises(ValueError, match='User must be logged in'):
            services: Services = Services(auth=auth, engine=my_session)

