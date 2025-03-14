from typing import Iterable
import datetime
import pytest
from ...auth import Authorization
from ...services import Services
from ...database import MyEngine
from ...database import Payment, Tax, User


# TODO: more tests - details github project
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

    def test_pay_taxes(self, monkeypatch, capsys, dict_of):
        services: Services = dict_of['services']
        engine: MyEngine = dict_of['engine']

        inputs: Iterable = iter(['y', '100'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        services.pay_taxes('water')

        captured_output = capsys.readouterr()
        assert 'paid successfully' in captured_output.out.strip()

        user: User | None = engine.session.query(User).filter_by(name=dict_of['user']['username']).first()
        assert user != None
        
        water_tax: Tax | None = next((tax for tax in user.taxes if tax.taxname == 'water'), None) 
        assert water_tax != None
        assert water_tax.payment_status == True

        provided_payments: list[Payment] = water_tax.payments
        today: str = datetime.date.today().strftime('%d-%m-%Y')
        our_payment: Payment | None = next(
            (payment for payment in provided_payments if (payment.date == today and payment.price == 100)),
            None)
        assert our_payment != None

    def test_pay_unexisting_taxes(self, monkeypatch, capsys, dict_of):
        services: Services = dict_of['services']
        engine: MyEngine = dict_of['engine']

        inputs: Iterable = iter(['y', '100'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        services.pay_taxes('eter')

        captured_output = capsys.readouterr()
        assert ' not found, attempting to add tax' in captured_output.out.strip()
        assert 'paid successfully' in captured_output.out.strip()

        user: User | None = engine.session.query(User).filter_by(name=dict_of['user']['username']).first()
        assert user != None, 'User exsits?'
        
        water_tax: Tax | None = next((tax for tax in user.taxes if tax.taxname == 'eter'), None) 
        assert water_tax != None, 'Tax exists?'
        assert water_tax.payment_status == True, 'Tax paid?'

        provided_payments: list[Payment] = water_tax.payments
        today: str = datetime.date.today().strftime('%d-%m-%Y')
        our_payment: Payment | None = next(
            (payment for payment in provided_payments if (payment.date == today and payment.price == 100)),
            None)
        assert our_payment != None, 'Should be no payment here'

    def test_cancel_payment(self, monkeypatch, capsys, dict_of) -> None:
        services: Services = dict_of['services']
        engine: MyEngine = dict_of['engine']

        inputs: Iterable = iter(['n'] * 2)
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        services.pay_taxes('eter')

        captured_output = capsys.readouterr()
        assert 'Aborted' in captured_output.out.strip()
        assert 'paid successfully' not in captured_output.out.strip()

        user: User | None = engine.session.query(User).filter_by(name=dict_of['user']['username']).first()
        assert user != None, 'User should be exsisting'
        
        water_tax: Tax | None = next((tax for tax in user.taxes if tax.taxname == 'eter'), None) 
        assert water_tax == None, 'Tax should not exists'

        services.pay_taxes('water')

        captured_output = capsys.readouterr()
        assert 'Aborted' in captured_output.out.strip()
        assert 'paid successfully' not in captured_output.out.strip()

        user: User | None = engine.session.query(User).filter_by(name=dict_of['user']['username']).first()
        assert user != None, 'User should be exsisting'
        
        water_tax: Tax | None = next((tax for tax in user.taxes if tax.taxname == 'water'), None) 
        assert water_tax != None, 'Tax should exists'
        assert water_tax.payment_status == False, 'Tax shouln\'t be paid'

        provided_payments: list[Payment] = water_tax.payments
        today: str = datetime.date.today().strftime('%d-%m-%Y')
        our_payment: Payment | None = next(
            (payment for payment in provided_payments if (payment.date == today and payment.price == 100)),
            None)
        assert our_payment == None, 'There should be no payment'


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

