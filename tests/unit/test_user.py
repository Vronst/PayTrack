import pytest 
from paytrack.models import User


class TestPositiveUser:

    @pytest.mark.regression
    def test_creation_company_false(self, session):
        name: str = 'testuser'
        surname: str = 'testsurname'
        email: str = 'test@test.com'
        password: str = 'testpass'
        
        user: User = User(
                name=name,
                surname=surname,
                email=email,
                password=password
            )

        session.add(user)
        session.commit()

        assert user.name == name 
        assert user.surname == surname 
        assert user.email == email
        assert user.password == password
        assert user.company == False 
        assert user.premium == False 
        assert user.parent_id is None
        assert user.parent is None 
        assert user.phone is None 
        assert user.admin == False
        assert user.included == []
        assert user.subaccounts == []
        assert user.settings is None
        assert user.transactions == []
        assert user.included_in_transactions == []
        assert user.other_receivers == []
        assert user.savings is None
        assert user.subscriptions == []
        assert user.subscription_shares == []
        assert user.included_in_subscriptions == []
        assert user.transactions_shares == []
    # TODO: more creation tests

    @pytest.mark.regression
    def test_included_relationship(self, session, users) -> None:
        u1, u2, u3 = users

        u1.included.extend([u2, u3])

        session.add_all([u1, u2, u3])
        session.commit()

        assert u2 in u1.included
        assert u3 in u1.included

        assert u1 in u2.included_in
        assert u1 in u3.included_in

        assert u2.included == []
        assert u3.included == []

    @pytest.mark.regression
    def test_parent_and_child(self, session, users) -> None:
        u1, u2, u3 = users 
        
        session.add_all([u1, u2, u3])
        session.commit()
        assert u1.subaccounts == []
        u2.parent_id = u1.id 
        session.add(u2)
        session.commit()
        assert u1.subaccounts == [u2]

        u3.parent_id = u2.id 
        session.add(u3)
        session.commit()

        assert u1.parent == None 
        assert len(u1.subaccounts) == 1
        assert u2.subaccounts == [u3]
        assert u3.parent == u2


class TestNegativeUser:
    pass
