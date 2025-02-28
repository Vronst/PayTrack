from ...auth import Authorization
from ...services import Services


class TestServicesPositive:

    def test_check_taxes(self, capsys, my_session):
        username: str = 'check_taxes'
        password: str = 'StrongPass!'
        auth: Authorization = Authorization(engine=my_session, action='register', username=username, password=password)
        assert auth.user != None
        services: Services = Services(auth, my_session)

        services.check_taxes(simple=True)
        captured_output = capsys.readouterr()
        assert captured_output.out.strip() == ''
    
