from typing import Iterable, Any
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

        result: dict[int, Tax] = services.check_taxes()
        captured_output = capsys.readouterr()
        assert 'water' in captured_output.out.strip()
        assert '0' in captured_output.out.strip()
        assert isinstance(result, dict) == True

    def test_check_taxes_simple(self, capsys, my_session):
        username: str = 'checktaxessimple'
        password: str = 'StrongPass!'
        auth: Authorization = Authorization(engine=my_session, action='register', username=username, password=password)
        assert auth.user != None
        services: Services = Services(auth, my_session)

        result: dict[int, Tax] = services.check_taxes(simple=True)
        captured_output = capsys.readouterr()
        assert 'water' in captured_output.out.strip()
        assert '0' in captured_output.out.strip()
        assert isinstance(result, dict) == True

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
        assert water_tax is not None
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
        assert water_tax is not None, 'Tax exists?'
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
        assert water_tax is None, 'Tax should not exist'

        services.pay_taxes('water')

        captured_output = capsys.readouterr()
        assert 'Aborted' in captured_output.out.strip()
        assert 'paid successfully' not in captured_output.out.strip()

        user: User | None = engine.session.query(User).filter_by(name=dict_of['user']['username']).first()
        assert user != None, 'User should be exsisting'
        
        water_tax: Tax | None = next((tax for tax in user.taxes if tax.taxname == 'water'), None) 
        assert water_tax is not None, 'Tax should exists'
        assert water_tax.payment_status == False, 'Tax shouln\'t be paid'

        provided_payments: list[Payment] = water_tax.payments
        today: str = datetime.date.today().strftime('%d-%m-%Y')
        our_payment: Payment | None = next(
            (payment for payment in provided_payments if (payment.date == today and payment.price == 100)),
            None)
        assert our_payment == None, 'There should be no payment'

    def test_view_payments(self, dict_of, capsys, monkeypatch) -> None:
        services: Services = dict_of['services']

        inputs: Iterable = iter([''])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        services.view_payments('water')

        captured_output = capsys.readouterr()
        coe: str = captured_output.out.strip()
        assert 'ID' in coe
        assert 'Price' in coe
        assert 'not found' not in coe

    def test_edit_payment_cancel(self, dict_of, capsys, monkeypatch) -> None:
        services: Services = dict_of.get('services')
        inputs: Iterable = iter(['y', '100', 'q'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        services.pay_taxes('water')
        user_id: int = dict_of['engine'].session.query(User).filter_by(name=dict_of['user']['username']).first().id
        payment_id: int = dict_of['engine'].session.query(Payment).filter_by(users_id=user_id).first().id

        assert isinstance(payment_id, int)

        services.edit_payment(payment_id)
        captured_output = capsys.readouterr()
        coe: str = captured_output.out.strip()

        assert 'Selected payment is not found' not in coe
        assert 'ID' in coe
        assert 'Price' in coe

    def test_edit_payment_delete_payment(self, dict_of, capsys, monkeypatch) -> None:
        services: Services = dict_of.get('services')
        inputs: Iterable = iter(['y', '100', '2', 'Y'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        services.pay_taxes('water')
        user_id: int = dict_of['engine'].session.query(User).filter_by(name=dict_of['user']['username']).first().id
        payment_id: int = dict_of['engine'].session.query(Payment).filter_by(users_id=user_id).first().id

        assert isinstance(payment_id, int)

        services.edit_payment(payment_id)
        captured_output = capsys.readouterr()
        coe: str = captured_output.out.strip()

        assert 'Selected payment is not found' not in coe
        assert 'ID' in coe
        assert 'Price' in coe
        assert 'Removed successfully' in coe
        assert 'Canceled' not in coe
        assert dict_of['engine'].session.get(Payment, payment_id) is None

    def test_edit_payment_delete_payment_cancel(self, dict_of, capsys, monkeypatch) -> None:
        services: Services = dict_of.get('services')
        inputs: Iterable = iter(['y', '100', '2', 'n'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        services.pay_taxes('water')
        user_id: int = dict_of['engine'].session.query(User).filter_by(name=dict_of['user']['username']).first().id
        payment_id: int = dict_of['engine'].session.query(Payment).filter_by(users_id=user_id).first().id

        assert isinstance(payment_id, int)

        services.edit_payment(payment_id)
        captured_output = capsys.readouterr()
        coe: str = captured_output.out.strip()

        assert 'Selected payment is not found' not in coe
        assert 'ID' in coe
        assert 'Price' in coe
        assert 'Removed successfully' not in coe
        assert 'Canceled' in coe
        assert dict_of['engine'].session.get(Payment, payment_id) is not None

    def test_payment_edit_details(self, dict_of, capsys, monkeypatch) -> None:
        services: Services = dict_of.get('services')
        school_tax_id: int = next(tax for tax in services.user.taxes if tax.taxname == 'school').id
        inputs: Iterable = iter([
            'y', '100', '1', '1', '28', 'January', '1999', '2', '123', '3', str(school_tax_id), 'q', 'q'
        ])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        services.pay_taxes('water')
        user_id: int = dict_of['engine'].session.query(User).filter_by(name=dict_of['user']['username']).first().id
        payment_id: int = dict_of['engine'].session.query(Payment).filter_by(users_id=user_id).first().id
        assert isinstance(payment_id, int)

        services.edit_payment(payment_id)
        captured_output = capsys.readouterr()
        coe: str = captured_output.out.strip()
        our_payment: Payment = dict_of['engine'].session.get(Payment, payment_id)
        assert 'Selected payment is not found' not in coe
        assert 'ID' in coe
        assert 'Price' in coe
        assert 'Removed successfully' not in coe
        assert 'Canceled' not in coe
        assert our_payment is not None
        assert our_payment.price == 123
        assert our_payment.date == '28-01-1999'
        assert our_payment.tax.id == school_tax_id
        assert our_payment.tax.taxname == 'school'

    def test_payment_edit_details_delete_cancel(self, dict_of, capsys, monkeypatch) -> None:
        services: Services = dict_of.get('services')
        school_tax_id: int = next(tax for tax in services.user.taxes if tax.taxname == 'school').id
        inputs: Iterable = iter([
            'y', '100', '1', '4', 'n', 'q', 'q'
        ])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        services.pay_taxes('water')
        user_id: int = dict_of['engine'].session.query(User).filter_by(name=dict_of['user']['username']).first().id
        payment_id: int = dict_of['engine'].session.query(Payment).filter_by(users_id=user_id).first().id
        assert isinstance(payment_id, int)

        services.edit_payment(payment_id)
        captured_output = capsys.readouterr()
        coe: str = captured_output.out.strip()
        our_payment: Payment = dict_of['engine'].session.get(Payment, payment_id)
        assert 'Selected payment is not found' not in coe
        assert 'ID' in coe
        assert 'Price' in coe
        assert 'Deleted successfully' not in coe
        assert 'Canceled' in coe
        assert our_payment is not None
        assert our_payment.price == 100
        assert our_payment.tax.taxname == 'water'

    def test_payment_edit_details_delete(self, dict_of, capsys, monkeypatch) -> None:
        services: Services = dict_of.get('services')
        school_tax_id: int = next(tax for tax in services.user.taxes if tax.taxname == 'school').id
        inputs: Iterable = iter([
            'y', '100', '1', '4', 'Y', 'q'
        ])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        services.pay_taxes('water')
        user_id: int = dict_of['engine'].session.query(User).filter_by(name=dict_of['user']['username']).first().id
        payment_id: int = dict_of['engine'].session.query(Payment).filter_by(users_id=user_id).first().id
        assert isinstance(payment_id, int)

        services.edit_payment(payment_id)
        captured_output = capsys.readouterr()
        coe: str = captured_output.out.strip()
        our_payment: Payment = dict_of['engine'].session.get(Payment, payment_id)
        assert 'Selected payment is not found' not in coe
        assert 'ID' in coe
        assert 'Price' in coe
        assert 'Deleted successfully' in coe
        assert 'Canceled' not in coe
        assert our_payment is None

    def test_payment_edit_details_invalid_choice(self, dict_of, capsys, monkeypatch) -> None:
        services: Services = dict_of.get('services')
        school_tax_id: int = next(tax for tax in services.user.taxes if tax.taxname == 'school').id
        inputs: Iterable = iter([
            'y', '100', '1', '8', '28', 'January', '1999','a', 'q'
        ])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        services.pay_taxes('water')
        user_id: int = dict_of['engine'].session.query(User).filter_by(name=dict_of['user']['username']).first().id
        payment_id: int = dict_of['engine'].session.query(Payment).filter_by(users_id=user_id).first().id
        assert isinstance(payment_id, int)

        services.edit_payment(payment_id)
        captured_output = capsys.readouterr()
        coe: str = captured_output.out.strip()
        our_payment: Payment = dict_of['engine'].session.get(Payment, payment_id)
        assert 'Selected payment is not found' not in coe
        assert 'ID' in coe
        assert 'Price' in coe
        assert 'Removed successfully' not in coe
        assert 'Canceled' not in coe
        assert 'Abandoned changes' in coe
        assert our_payment is not None
        assert our_payment.price == 100
        assert our_payment.date == datetime.date.today().strftime('%d-%m-%Y')
        assert our_payment.tax.taxname == 'water'

    def test_payment_edit_details_abandon(self, dict_of, capsys, monkeypatch) -> None:
        services: Services = dict_of.get('services')
        school_tax_id: int = next(tax for tax in services.user.taxes if tax.taxname == 'school').id
        inputs: Iterable = iter([
            'y', '100', '1', '1', '28', 'January', '1999', '2', '123', '3', str(school_tax_id), 'a', 'q'
        ])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        services.pay_taxes('water')
        user_id: int = dict_of['engine'].session.query(User).filter_by(name=dict_of['user']['username']).first().id
        payment_id: int = dict_of['engine'].session.query(Payment).filter_by(users_id=user_id).first().id
        assert isinstance(payment_id, int)

        services.edit_payment(payment_id)
        captured_output = capsys.readouterr()
        coe: str = captured_output.out.strip()
        our_payment: Payment = dict_of['engine'].session.get(Payment, payment_id)
        assert 'Selected payment is not found' not in coe
        assert 'ID' in coe
        assert 'Price' in coe
        assert 'Removed successfully' not in coe
        assert 'Canceled' not in coe
        assert 'Abandoned changes' in coe
        assert our_payment is not None
        assert our_payment.price == 100
        assert our_payment.date == datetime.date.today().strftime('%d-%m-%Y')
        assert our_payment.tax.taxname == 'water'

    def test_update_method(self, dict_of, monkeypatch) -> None:
        services: Services = dict_of['services']
        engine: MyEngine = dict_of['engine']
        day, month, year = datetime.date.today().strftime('%d-%m-%Y').split('-')

        inputs: Iterable = iter(['y', '1500', ])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        services.pay_taxes('water')
        user: User = services.user
        all_taxes: list[Tax] = user.taxes
        selected_tax: Tax = next(tax for tax in all_taxes if tax.taxname == 'water')
        assert selected_tax.payment_status == True
        payments: list[Payment] = selected_tax.payments
        our_payment: Payment = next(payment for payment in payments if payment.taxes_id == selected_tax.id)
        our_payment.date = f'{day}-{int(month)-1}-{year}'
        engine.session.add(our_payment)
        engine.session.commit()
        services.update()
        assert selected_tax.payment_status == False
        our_payment.date = f'{day}-{int( month )+1}-{year}'
        engine.session.add(our_payment)
        engine.session.commit()
        services.update()
        assert selected_tax.payment_status == True, 'Paid to one year later, should be true'

class TestServicesNegative:
    def test_changing_unchangable_attributes_auth(self, dict_of) -> None:
        services: Services = dict_of['services']

        with pytest.raises(AttributeError, match='This attribute cannot be changed directly'):
            services.auth = Authorization(engine=dict_of['engine'])

    def test_changing_unchangable_attributes_engine(self, dict_of) -> None:
        services: Services = dict_of['services']

        with pytest.raises(AttributeError, match='This attribute cannot be changed directly'):
            services.engine = dict_of['engine']
            
    def test_changing_unchangable_attributes(self, my_session) -> None:
        username: str = 'TCua'
        password: str = 'StrongPass!'
        auth: Authorization = Authorization(engine=my_session, action='register', username=username, password=password)
        services: Services = Services(auth=auth, engine=my_session)

        with pytest.raises(AttributeError, match='This attribute cannot be changed directly'):
            services.auth = Authorization(engine=MyEngine())

        with pytest.raises(AttributeError, match='This attribute cannot be changed directly'):
            services.engine = MyEngine()

    def test_check_taxes_not_logged_in(self, my_session, capsys, monkeypatch) -> None:
        username: str = 'tctnli11'
        password: str = 'StrongPass!'
        my_session.create_user(username=username, password=password)
        auth: Authorization = Authorization(engine=my_session)
        services: Services = Services(auth=auth, engine=my_session)

        inputs: Iterable = iter([username, password])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        services.check_taxes()
        captured_output = capsys.readouterr()
        coe: str = captured_output.out.strip()
        assert 'You must log in to use services!' in coe
        # assert 'Username:' in coe
        assert 'Tax' in coe
        assert 'Is paid?' in coe

    def test_check_taxes_not_logged_in_second_try(self, my_session, capsys, monkeypatch) -> None:
        username: str = 'tctnli11'
        password: str = 'StrongPass!'
        my_session.create_user(username=username, password=password)
        auth: Authorization = Authorization(engine=my_session)
        services: Services = Services(auth=auth, engine=my_session)

        inputs: Iterable = iter(['wrongusername', 'wrongpass', username, password])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        services.check_taxes()
        captured_output = capsys.readouterr()
        coe: str = captured_output.out.strip()
        assert 'You must log in to use services!' in coe
        # assert 'Username:' in coe
        assert 'Tax' in coe
        assert 'Is paid?' in coe

    def test_pay_taxes_no_float(self, monkeypatch, dict_of):
        services: Services = dict_of['services']
        engine: MyEngine = dict_of['engine']

        inputs: Iterable = iter(['y', 'Pszemek'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        with pytest.raises(ValueError, match='could not convert'):
            services.pay_taxes('water')

        user: User | None = engine.session.query(User).filter_by(name=dict_of['user']['username']).first()
        assert user != None
        
        water_tax: Tax | None = next((tax for tax in user.taxes if tax.taxname == 'water'), None) 
        assert water_tax is not None
        assert water_tax.payment_status == False

        provided_payments: list[Payment] = water_tax.payments
        today: str = datetime.date.today().strftime('%d-%m-%Y')
        our_payment: Payment | None = next(
            (payment for payment in provided_payments if (payment.date == today and payment.price == 100)),
            None)
        assert our_payment == None

    def test_view_payments_while_no_taxes(self, dict_of, capsys) -> None:
        services: Services = dict_of['services']
        auth: Authorization = dict_of['auth']
        # auth.logout()
        # auth.login(username=dict_of['user_no_taxes']['username'], password=dict_of['user_no_taxes']['password'])

        services.view_payments('whatisthistax')
        captured_output = capsys.readouterr()
        coe: str = captured_output.out.strip()
        assert 'not found' in coe

    def test_view_payments_while_no_taxes2(self, dict_of, capsys) -> None:
        services: Services = dict_of['services']
        auth: Authorization = dict_of['auth']
        auth.logout()
        auth.login(username=dict_of['user_no_taxes']['username'], password=dict_of['user_no_taxes']['password'])

        result: None = services.view_payments('water')  #  basic tax, should exist normally
        assert result is None
        captured_output = capsys.readouterr()
        coe: str = captured_output.out.strip()
        assert 'not found' in coe

    def test_view_payments_unknown_choice(self, dict_of, capsys, monkeypatch) -> None:
        services: Services = dict_of['services']

        inputs: Iterable = iter(['Spain'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        services.view_payments('water')

        captured_output = capsys.readouterr()
        coe: str = captured_output.out.strip()
        assert 'ID' in coe
        assert 'Price' in coe
        assert 'not found' not in coe
        assert 'Unknown choice' in coe
        

    def test_view_payments_not_exsiting_tax(self, dict_of, capsys) -> None:
        services: Services = dict_of['services']

        services.view_payments('Spain')

        captured_output = capsys.readouterr()
        coe: str = captured_output.out.strip()
        assert 'ID' not in coe
        assert 'Price' not in coe
        assert 'not found' in coe
        assert 'Unknown choice' not in coe

    def test_edit_payment_cancel_invalid_option(self, dict_of, capsys, monkeypatch) -> None:
        services: Services = dict_of.get('services')
        inputs: Iterable = iter(['y', '100', 'whatisthis', 'quit'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        services.pay_taxes('water')
        user_id: int = dict_of['engine'].session.query(User).filter_by(name=dict_of['user']['username']).first().id
        payment_id: int = dict_of['engine'].session.query(Payment).filter_by(users_id=user_id).first().id

        assert isinstance(payment_id, int)

        services.edit_payment(payment_id)
        captured_output = capsys.readouterr()
        coe: str = captured_output.out.strip()

        assert 'Selected payment is not found' not in coe
        assert 'ID' in coe
        assert 'Price' in coe
        assert 'Invalid option' in coe

    def test_payment_edit_details_value_error(self, dict_of, capsys, monkeypatch) -> None:
        services: Services = dict_of.get('services')
        school_tax_id: int = next(tax for tax in services.user.taxes if tax.taxname == 'school').id
        inputs: Iterable = iter([
            'y', '100', '1', '1'] + ['lol', 'January', '1999']+ ['1', '28', 'nonmonth', '1999'] +
            ['1', '28', '1', 'myyear'] + ['q', 'q'
        ])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        services.pay_taxes('water')
        user_id: int = dict_of['engine'].session.query(User).filter_by(name=dict_of['user']['username']).first().id
        payment_id: int = dict_of['engine'].session.query(Payment).filter_by(users_id=user_id).first().id
        assert isinstance(payment_id, int)

        services.edit_payment(payment_id)
        captured_output = capsys.readouterr()
        coe: str = captured_output.out.strip()
        our_payment: Payment = dict_of['engine'].session.get(Payment, payment_id)
        assert 'Selected payment is not found' not in coe
        assert 'ID' in coe
        assert 'Price' in coe
        assert 'Removed successfully' not in coe
        assert 'Canceled' not in coe
        assert 'invalid literal for int() with base 10: \'lol\'' in coe
        assert 'This is not a month: nonmonth' in coe.split('\n')
        assert 'invalid literal for int() with base 10: \'myyear\''in coe
        assert our_payment is not None
        assert our_payment.price == 100
        assert our_payment.date == datetime.date.today().strftime('%d-%m-%Y')
        assert our_payment.tax.taxname == 'water'

    def test_payment_edit_details_second_option_value_error(self, dict_of, capsys, monkeypatch) -> None:
        services: Services = dict_of.get('services')
        school_tax_id: int = next(tax for tax in services.user.taxes if tax.taxname == 'school').id
        inputs: Iterable = iter([
            'y', '100', '1', '2'] + ['lol']+ ['2', '11p'] +
            ['q', 'q'
        ])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        services.pay_taxes('water')
        user_id: int = dict_of['engine'].session.query(User).filter_by(name=dict_of['user']['username']).first().id
        payment_id: int = dict_of['engine'].session.query(Payment).filter_by(users_id=user_id).first().id
        assert isinstance(payment_id, int)

        services.edit_payment(payment_id)
        captured_output = capsys.readouterr()
        coe: str = captured_output.out.strip()
        our_payment: Payment = dict_of['engine'].session.get(Payment, payment_id)
        assert 'Selected payment is not found' not in coe
        assert 'ID' in coe
        assert 'Price' in coe
        assert 'Removed successfully' not in coe
        assert 'Canceled' not in coe
        assert 'invalid literal for int() with base 10: \'lol\'' in coe
        assert 'invalid literal for int() with base 10: \'11p\''in coe
        assert our_payment is not None
        assert our_payment.price == 100
        assert our_payment.date == datetime.date.today().strftime('%d-%m-%Y')
        assert our_payment.tax.taxname == 'water'


    def test_payment_edit_details_third_option_value_error(self, dict_of, capsys, monkeypatch) -> None:
        services: Services = dict_of.get('services')
        school_tax_id: int = next(tax for tax in services.user.taxes if tax.taxname == 'school').id
        inputs: Iterable = iter([
            'y', '100', '1', '3'] + ['lol']+ ['3', '11p'] + ['3', '1111111111111111'] +
            ['q', 'q'
        ])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        services.pay_taxes('water')
        user_id: int = dict_of['engine'].session.query(User).filter_by(name=dict_of['user']['username']).first().id
        payment_id: int = dict_of['engine'].session.query(Payment).filter_by(users_id=user_id).first().id
        assert isinstance(payment_id, int)

        services.edit_payment(payment_id)
        captured_output = capsys.readouterr()
        coe: str = captured_output.out.strip()
        our_payment: Payment = dict_of['engine'].session.get(Payment, payment_id)
        assert 'Selected payment is not found' not in coe
        assert 'ID' in coe
        assert 'Price' in coe
        assert 'Removed successfully' not in coe
        assert 'Canceled' not in coe
        assert 'Error occured:\ninvalid literal for int() with base 10: \'lol\'' in coe
        assert 'Error occured:\ninvalid literal for int() with base 10: \'11p\'' in coe
        assert 'Id out of range' in coe
        assert our_payment is not None
        assert our_payment.price == 100
        assert our_payment.date == datetime.date.today().strftime('%d-%m-%Y')
        assert our_payment.tax.taxname == 'water'


