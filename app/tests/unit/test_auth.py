from ...auth import Authorization


class TestAuthorizationPositive:

    def test_empty_init(self, my_session) -> None:
        auth: Authorization = Authorization(session=my_session)

        assert auth.user == None
        assert auth.guest == []
        assert auth.guest_list == []

    def test_register_init(self) -> None:
        ...

    def test_login_init(self) -> None:
        ...

    def test_logout(self) -> None:
        ...
