from typing import Iterable
import datetime
import pytest

from paytrack.app.utils import LoginError
from paytrack.app.services import Services
from paytrack.app.database import MyEngine
from paytrack.app.database import Payment, Tax, User
from paytrack.app.auth import Authorization


class TestServicesPositive:

    def test_check_taxes(self, capsys, my_session):
        username: str = 'checktaxes'
        password: str = 'StrongPass!'
        auth: Authorization = Authorization(engine=my_session, action='register', username=username, password=password)
        assert auth.user != None
        assert auth.user.taxes != []
        services: Services = Services(auth.user, my_session)
        result: dict[int, Tax] = services.check_taxes(simple=True)
        captured_output = capsys.readouterr()
        assert 'water' in captured_output.out.strip()
        assert '0' in captured_output.out.strip()
        assert isinstance(result, dict) == True

    def test_check_taxes_simple(self, capsys, my_session):
        username: str = 'checktaxessimple'
        password: str = 'StrongPass!'
        auth: Authorization = Authorization(engine=my_session, username=username, password=password, action='register')
        assert auth.user != None
        services: Services = Services(auth.user, my_session)

        result: dict[int, Tax] = services.check_taxes(simple=True)
        captured_output = capsys.readouterr()
        assert 'water' in captured_output.out.strip()
        assert '0' in captured_output.out.strip()
        assert isinstance(result, dict) == True

    def test_pay_taxes(self, capsys, my_session):
        username: str = 'checktaxessimple'
        password: str = 'StrongPass!'
        auth: Authorization = Authorization(engine=my_session, username=username, password=password, action='register')
        assert auth.user is not None
        services: Services = Services(auth.user, my_session)
        engine: MyEngine = my_session

        inputs: Iterable = iter(['y', '100'])

        services.pay_taxes('water', input_method=lambda _: next(inputs))

        captured_output = capsys.readouterr()
        assert 'paid successfully' in captured_output.out.strip()

        user: User | None = engine.session.query(User).filter_by(name=username).first()
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

    def test_pay_unexisting_taxes(self, capsys, my_session):
        username: str = 'checktaxessimple'
        password: str = 'StrongPass!'
        auth: Authorization = Authorization(engine=my_session, username=username, password=password, action='register')
        assert auth.user is not None
        services: Services = Services(auth.user, my_session)
        engine: MyEngine = my_session

        inputs: Iterable = iter(['y', '100'])

        services.pay_taxes('eter', input_method=lambda _: next(inputs))

        captured_output = capsys.readouterr()
        assert ' not found, attempting to add tax' in captured_output.out.strip()
        assert 'paid successfully' in captured_output.out.strip()

        user: User | None = engine.session.query(User).filter_by(name=username).first()
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

    def test_cancel_payment(self, capsys, my_session) -> None:
        username: str = 'checktaxessimple'
        password: str = 'StrongPass!'
        auth: Authorization = Authorization(engine=my_session, username=username, password=password, action='register')
        assert auth.user is not None
        services: Services = Services(auth.user, my_session)
        engine: MyEngine = my_session

        inputs: Iterable = iter(['n'] * 2)

        services.pay_taxes('eter', input_method=lambda _: next(inputs))

        captured_output = capsys.readouterr()
        assert 'Aborted' in captured_output.out.strip()
        assert 'paid successfully' not in captured_output.out.strip()

        user: User | None = engine.session.query(User).filter_by(name=username).first()
        assert user != None, 'User should be exsisting'
        
        water_tax: Tax | None = next((tax for tax in user.taxes if tax.taxname == 'eter'), None) 
        assert water_tax is None, 'Tax should not exist'

        services.pay_taxes('water', input_method=lambda _: next(inputs))

        captured_output = capsys.readouterr()
        assert 'Aborted' in captured_output.out.strip()
        assert 'paid successfully' not in captured_output.out.strip()

        user: User | None = engine.session.query(User).filter_by(name=username).first()
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

    def test_view_payments(self, my_session, capsys) -> None:
        username: str = 'checktaxessimple'
        password: str = 'StrongPass!'
        auth: Authorization = Authorization(engine=my_session, username=username, password=password, action='register')
        assert auth.user is not None
        services: Services = Services(auth.user, my_session)

        inputs: Iterable = iter([''])

        services.view_payments('water', input_method=lambda _: next(inputs))

        captured_output = capsys.readouterr()
        coe: str = captured_output.out.strip()
        assert 'ID' in coe
        assert 'Price' in coe
        assert 'not found' not in coe

    def test_edit_payment_cancel(self, my_session, capsys) -> None:
        username: str = 'checktaxessimple'
        password: str = 'StrongPass!'
        auth: Authorization = Authorization(engine=my_session, username=username, password=password, action='register')
        assert auth.user is not None
        services: Services = Services(auth.user, my_session)
        inputs: Iterable = iter(['y', '100', 'q'])
        services.pay_taxes('water', input_method=lambda _: next(inputs))
        user_id: int = my_session.session.query(User).filter_by(name=username).first().id
        payment_id: int = my_session.session.query(Payment).filter_by(users_id=user_id).first().id

        assert isinstance(payment_id, int)

        services.edit_payment(payment_id, input_method=lambda _: next(inputs))
        captured_output = capsys.readouterr()
        coe: str = captured_output.out.strip()

        assert 'Selected payment is not found' not in coe
        assert 'ID' in coe
        assert 'Price' in coe

    def test_edit_payment_delete_payment(self, my_session, capsys) -> None:
        username: str = 'checktaxessimple'
        password: str = 'StrongPass!'
        auth: Authorization = Authorization(engine=my_session, username=username, password=password, action='register')
        assert auth.user is not None
        services: Services = Services(auth.user, my_session)
        inputs: Iterable = iter(['y', '100', '2', 'Y'])
        services.pay_taxes('water', input_method=lambda _: next(inputs))
        user_id: int = my_session.session.query(User).filter_by(name=username).first().id
        payment_id: int = my_session.session.query(Payment).filter_by(users_id=user_id).first().id

        assert isinstance(payment_id, int)

        services.edit_payment(payment_id, input_method=lambda _: next(inputs))
        captured_output = capsys.readouterr()
        coe: str = captured_output.out.strip()

        assert 'Selected payment is not found' not in coe
        assert 'ID' in coe
        assert 'Price' in coe
        assert 'Removed successfully' in coe
        assert 'Canceled' not in coe
        assert my_session.session.get(Payment, payment_id) is None

    def test_edit_payment_delete_payment_cancel(self, my_session, capsys) -> None:
        username: str = 'checktaxessimple'
        password: str = 'StrongPass!'
        auth: Authorization = Authorization(engine=my_session, username=username, password=password, action='register')
        assert auth.user is not None
        services: Services = Services(auth.user, my_session)
        inputs: Iterable = iter(['y', '100', '2', 'n'])
        services.pay_taxes('water', input_method=lambda _: next(inputs))
        user_id: int = my_session.session.query(User).filter_by(name=username).first().id
        payment_id: int = my_session.session.query(Payment).filter_by(users_id=user_id).first().id

        assert isinstance(payment_id, int)

        services.edit_payment(payment_id, input_method=lambda _: next(inputs))
        captured_output = capsys.readouterr()
        coe: str = captured_output.out.strip()

        assert 'Selected payment is not found' not in coe
        assert 'ID' in coe
        assert 'Price' in coe
        assert 'Removed successfully' not in coe
        assert 'Canceled' in coe
        assert my_session.session.get(Payment, payment_id) is not None

    def test_payment_edit_details(self, my_session, capsys) -> None:
        username: str = 'checktaxessimple'
        password: str = 'StrongPass!'
        auth: Authorization = Authorization(engine=my_session, username=username, password=password, action='register')
        assert auth.user is not None
        services: Services = Services(auth.user, my_session)
        school_tax_id: int = next(tax for tax in services.user.taxes if tax.taxname == 'school').id
        inputs: Iterable = iter([
            'y', '100', '1', '1', '28', 'January', '1999', '2', '123', '3', str(school_tax_id), 'q', 'q'
        ])
        services.pay_taxes('water', input_method=lambda _: next(inputs))
        user_id: int = my_session.session.query(User).filter_by(name=username).first().id
        payment_id: int = my_session.session.query(Payment).filter_by(users_id=user_id).first().id
        assert isinstance(payment_id, int)

        services.edit_payment(payment_id, input_method=lambda _: next(inputs))
        our_payment: Payment = my_session.session.get(Payment, payment_id)

        captured_output = capsys.readouterr()
        coe: str = captured_output.out.strip()
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

    def test_payment_edit_details_delete_cancel(self, my_session, capsys) -> None:
        username: str = 'checktaxessimple'
        password: str = 'StrongPass!'
        auth: Authorization = Authorization(engine=my_session, username=username, password=password, action='register')
        assert auth.user is not None
        services: Services = Services(auth.user, my_session)
        inputs: Iterable = iter([
            'y', '100', '1', '4', 'n', 'q', 'q'
        ])
        services.pay_taxes('water', input_method=lambda _: next(inputs))
        user_id: int = my_session.session.query(User).filter_by(name=username).first().id
        payment_id: int = my_session.session.query(Payment).filter_by(users_id=user_id).first().id
        assert isinstance(payment_id, int)

        services.edit_payment(payment_id, input_method=lambda _: next(inputs))
        captured_output = capsys.readouterr()
        coe: str = captured_output.out.strip()
        our_payment: Payment = my_session.session.get(Payment, payment_id)
        assert 'Selected payment is not found' not in coe
        assert 'ID' in coe
        assert 'Price' in coe
        assert 'Deleted successfully' not in coe
        assert 'Canceled' in coe
        assert our_payment is not None
        assert our_payment.price == 100
        assert our_payment.tax.taxname == 'water'

    def test_payment_edit_details_delete(self, my_session, capsys) -> None:
        username: str = 'checktaxessimple'
        password: str = 'StrongPass!'
        auth: Authorization = Authorization(engine=my_session, username=username, password=password, action='register')
        assert auth.user is not None
        services: Services = Services(auth.user, my_session)
        inputs: Iterable = iter([
            'y', '100', '1', '4', 'Y', 'q'
        ])
        services.pay_taxes('water', input_method=lambda _: next(inputs))
        user_id: int = my_session.session.query(User).filter_by(name=username).first().id
        payment_id: int = my_session.session.query(Payment).filter_by(users_id=user_id).first().id
        assert isinstance(payment_id, int)

        services.edit_payment(payment_id, input_method=lambda _: next(inputs))
        captured_output = capsys.readouterr()
        coe: str = captured_output.out.strip()
        our_payment: Payment = my_session.session.get(Payment, payment_id)
        assert 'Selected payment is not found' not in coe
        assert 'ID' in coe
        assert 'Price' in coe
        assert 'Deleted successfully' in coe
        assert 'Canceled' not in coe
        assert our_payment is None

    def test_payment_edit_details_invalid_choice(self, my_session, capsys) -> None:
        username: str = 'checktaxessimple'
        password: str = 'StrongPass!'
        auth: Authorization = Authorization(engine=my_session, username=username, password=password, action='register')
        assert auth.user is not None
        services: Services = Services(auth.user, my_session)
        inputs: Iterable = iter([
            'y', '100', '1', '8', '28', 'January', '1999','a', 'q'
        ])
        services.pay_taxes('water', input_method=lambda _: next(inputs))
        user_id: int = my_session.session.query(User).filter_by(name=username).first().id
        payment_id: int = my_session.session.query(Payment).filter_by(users_id=user_id).first().id
        assert isinstance(payment_id, int)

        services.edit_payment(payment_id, input_method=lambda _: next(inputs))
        captured_output = capsys.readouterr()
        coe: str = captured_output.out.strip()
        our_payment: Payment = my_session.session.get(Payment, payment_id)
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

    def test_payment_edit_details_abandon(self, my_session, capsys) -> None:
        username: str = 'checktaxessimple'
        password: str = 'StrongPass!'
        auth: Authorization = Authorization(engine=my_session, username=username, password=password, action='register')
        assert auth.user is not None
        services: Services = Services(auth.user, my_session)
        school_tax_id: int = next(tax for tax in services.user.taxes if tax.taxname == 'school').id
        inputs: Iterable = iter([
            'y', '100', '1', '1', '28', 'January', '1999', '2', '123', '3', str(school_tax_id), 'a', 'q'
        ])
        services.pay_taxes('water', input_method=lambda _: next(inputs))
        user_id: int = my_session.session.query(User).filter_by(name=username).first().id
        payment_id: int = my_session.session.query(Payment).filter_by(users_id=user_id).first().id
        assert isinstance(payment_id, int)

        services.edit_payment(payment_id, input_method=lambda _: next(inputs))
        captured_output = capsys.readouterr()
        coe: str = captured_output.out.strip()
        our_payment: Payment = my_session.session.get(Payment, payment_id)
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

    def test_update_method(self, my_session) -> None:
        username: str = 'checktaxessimple'
        password: str = 'StrongPass!'
        auth: Authorization = Authorization(engine=my_session, username=username, password=password, action='register')
        assert auth.user is not None
        services: Services = Services(auth.user, my_session)
        engine: MyEngine = my_session 
        day, month, year = datetime.date.today().strftime('%d-%m-%Y').split('-')

        inputs: Iterable = iter(['y', '1500', ])

        services.pay_taxes('water', input_method=lambda _: next(inputs))
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

    def test_delete_tax(self, my_session, capsys) -> None:
        username: str = 'checktaxessimple'
        password: str = 'StrongPass!'
        auth: Authorization = Authorization(engine=my_session, username=username, password=password, action='register')
        assert auth.user is not None
        services: Services = Services(auth.user, my_session)
        user: User | None = my_session.get_user(username=username)
        inputs: Iterable = iter(['Y'])
        assert user is not None
        taxname: str = user.taxes[0].taxname
        services.delete_tax(taxname=taxname, input_method=lambda _: next(inputs))
        captured_output: str = capsys.readouterr().out.strip()
        assert 'Deleted successfully' in captured_output
        assert not any(tax for tax in user.taxes if tax.taxname == taxname)

    def test_delete_tax_canceled(self, my_session, capsys) -> None:
        username: str = 'checktaxessimple'
        password: str = 'StrongPass!'
        auth: Authorization = Authorization(engine=my_session, username=username, password=password, action='register')
        assert auth.user is not None
        services: Services = Services(auth.user, my_session)
        user: User | None = my_session.get_user(username=username)
        inputs: Iterable = iter(['n'])
        assert user is not None
        taxname: str = user.taxes[0].taxname
        services.delete_tax(taxname=taxname, input_method=lambda _: next(inputs))
        captured_output: str = capsys.readouterr().out.strip()
        assert 'Canceled' in captured_output
        assert any(tax for tax in user.taxes if tax.taxname == taxname)

    def test_delete_tax_by_id(self, my_session, capsys) -> None:
        username: str = 'checktaxessimple'
        password: str = 'StrongPass!'
        auth: Authorization = Authorization(engine=my_session, username=username, password=password, action='register')
        assert auth.user is not None
        services: Services = Services(auth.user, my_session)
        user: User | None = my_session.get_user(username=username)
        inputs: Iterable = iter(['Y'])
        assert user is not None
        tax_id: int = user.taxes[0].id
        services.delete_tax(tax_id=tax_id, input_method=lambda _: next(inputs))
        captured_output: str = capsys.readouterr().out.strip()
        assert 'Deleted successfully' in captured_output
        assert not any(tax for tax in user.taxes if tax.id == tax_id)

    def test_add_tax(self, my_session, capsys) -> None:
        username: str = 'checktaxessimple'
        password: str = 'StrongPass!'
        auth: Authorization = Authorization(engine=my_session, username=username, password=password, action='register')
        assert auth.user is not None
        services: Services = Services(auth.user, my_session)
        user: User | None = my_session.get_user(username=username)
        assert user is not None
        taxname: str = 'testtax'
        inputs: Iterable = iter(['y'])
        services.add_tax(taxname=taxname, input_method=lambda _: next(inputs))
        captured_output: str = capsys.readouterr().out.strip()
        user_taxes: list[Tax] = user.taxes

        assert 'added successfully' in captured_output
        assert any(tax for tax in user_taxes if tax.taxname == taxname)

    def test_add_tax_and_cancel(self, my_session, capsys) -> None:
        username: str = 'checktaxessimple'
        password: str = 'StrongPass!'
        auth: Authorization = Authorization(engine=my_session, username=username, password=password, action='register')
        assert auth.user is not None
        services: Services = Services(auth.user, my_session)
        user: User | None = my_session.get_user(username=username)
        assert user is not None
        taxname: str = 'testtax'
        inputs: Iterable = iter(['n'])
        services.add_tax(taxname=taxname, input_method=lambda _: next(inputs))
        captured_output: str = capsys.readouterr().out.strip()
        user_taxes: list[Tax] = user.taxes

        assert 'Canceled' in captured_output
        assert not any(tax for tax in user_taxes if tax.taxname == taxname)

    def test_edit_tax(self, my_session, capsys) -> None:
        username: str = 'checktaxessimple'
        password: str = 'StrongPass!'
        auth: Authorization = Authorization(engine=my_session, username=username, password=password, action='register')
        assert auth.user is not None
        services: Services = Services(auth.user, my_session)
        user: User | None = my_session.get_user(username=username)
        assert user is not None
        taxname: str = user.taxes[0].taxname
        inputs: Iterable = iter(['new_name', 'y'])
        services.edit_tax(taxname=taxname, input_method=lambda _: next(inputs))
        captured_output: str = capsys.readouterr().out.strip()
        user_taxes: list[Tax] = my_session.get_user(username).taxes

        assert 'edited successfully' in captured_output
        assert not any(tax for tax in user_taxes if tax.taxname == taxname)
        assert any(tax for tax in user_taxes if tax.taxname == 'new_name')

    def test_edit_tax_by_id(self, my_session, capsys) -> None:
        username: str = 'checktaxessimple'
        password: str = 'StrongPass!'
        auth: Authorization = Authorization(engine=my_session, username=username, password=password, action='register')
        assert auth.user is not None
        services: Services = Services(auth.user, my_session)
        user: User | None = my_session.get_user(username=username)
        assert user is not None
        tax_id: int = user.taxes[0].id
        taxname: str = 'testtax'
        inputs: Iterable = iter([taxname, 'y'])
        services.edit_tax(tax_id=tax_id, input_method=lambda _: next(inputs))
        captured_output: str = capsys.readouterr().out.strip()
        user_taxes: list[Tax] = my_session.get_user(username).taxes

        assert 'edited successfully' in captured_output
        assert any(tax for tax in user_taxes if tax.taxname == taxname)


class TestServicesNegative:
    def test_changing_unchangable_attributes_auth(self, my_session, normal_user) -> None:
        username: str = 'checktaxessimple'
        password: str = 'StrongPass!'
        auth: Authorization = Authorization(engine=my_session, username=username, password=password, action='register')
        assert auth.user is not None
        services: Services = Services(auth.user, my_session)

        with pytest.raises(AttributeError, match='This attribute cannot be changed directly'):
            services.user = normal_user

    def test_changing_unchangable_attributes_engine(self, my_session, normal_user, no_session) -> None:
        services: Services = Services(normal_user, my_session)

        with pytest.raises(AttributeError, match='This attribute cannot be changed directly'):
            services.engine = no_session

    def test_check_taxes_not_logged_in(self, my_session) -> None:
        username: str = 'tctnli11'
        password: str = 'StrongPass!'
        my_session.create_user(username=username, password=password)
        auth: Authorization = Authorization(engine=my_session)
        with pytest.raises(LoginError, match='Before accessing services, log in'):
            # assert auth.user is not None
            services: Services = Services(auth.user, engine=my_session)
            services.check_taxes()

    def test_check_taxes_not_logged_in_second_try(self, my_session) -> None:
        username: str = 'tctnli11'
        password: str = 'StrongPass!'
        my_session.create_user(username=username, password=password)
        auth: Authorization = Authorization(engine=my_session)
        with pytest.raises(LoginError, match='Before accessing services, log in'):
            # assert auth.user is not None
            services: Services = Services(auth.user, engine=my_session)
            services.check_taxes()

    def test_pay_taxes_no_float(self, my_session):
        username: str = 'checktaxessimple'
        password: str = 'StrongPass!'
        auth: Authorization = Authorization(engine=my_session, username=username, password=password, action='register')
        assert auth.user is not None
        services: Services = Services(auth.user, my_session)
        engine: MyEngine = my_session

        inputs: Iterable = iter(['y', 'Pszemek'])
        with pytest.raises(ValueError, match='could not convert'):
            services.pay_taxes('water', input_method=lambda _: next(inputs))

        user: User | None = engine.session.query(User).filter_by(name=username).first()
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

    def test_view_payments_while_no_taxes(self,dict_of, capsys, my_session) -> None:
        auth: Authorization = Authorization(engine=my_session)
        auth.login(username=dict_of['user_no_taxes']['username'], password=dict_of['user_no_taxes']['password'])
        assert auth.user is not None
        services: Services = Services(auth.user, my_session)

        services.view_payments('water')
        captured_output = capsys.readouterr()
        coe: str = captured_output.out.strip()
        assert 'not found' in coe

    def test_view_payments_while_no_taxes2(self, capsys, my_session) -> None:
        username: str = 'thatisusername'
        password: str = 'Stronpass!'
        my_session.create_user(username, password, with_taxes=False)
        auth: Authorization = Authorization(engine=my_session, action='login', username=username, password=password)
        assert auth.user is not None
        services: Services = Services(auth.user, my_session)

        result: None = services.view_payments('water')  #  basic tax, should exist normally
        assert result is None
        captured_output = capsys.readouterr()
        coe: str = captured_output.out.strip()
        assert 'not found' in coe

    def test_view_payments_unknown_choice(self, my_session, capsys) -> None:
        username: str = 'checktaxessimple'
        password: str = 'StrongPass!'
        auth: Authorization = Authorization(engine=my_session, username=username, password=password, action='register')
        assert auth.user is not None
        services: Services = Services(auth.user, my_session)

        inputs: Iterable = iter(['Spain'])

        services.view_payments('water', input_method=lambda _: next(inputs))

        captured_output = capsys.readouterr()
        coe: str = captured_output.out.strip()
        assert 'ID' in coe
        assert 'Price' in coe
        assert 'not found' not in coe
        assert 'Unknown choice' in coe
        

    def test_view_payments_not_exsiting_tax(self, my_session, capsys) -> None:
        username: str = 'checktaxessimple'
        password: str = 'StrongPass!'
        auth: Authorization = Authorization(engine=my_session, username=username, password=password, action='register')
        assert auth.user is not None
        services: Services = Services(auth.user, my_session)

        services.view_payments('Spain')

        captured_output = capsys.readouterr()
        coe: str = captured_output.out.strip()
        assert 'ID' not in coe
        assert 'Price' not in coe
        assert 'not found' in coe
        assert 'Unknown choice' not in coe

    def test_edit_payment_cancel_invalid_option(self, my_session, capsys) -> None:
        username: str = 'checktaxessimple'
        password: str = 'StrongPass!'
        auth: Authorization = Authorization(engine=my_session, username=username, password=password, action='register')
        assert auth.user is not None
        services: Services = Services(auth.user, my_session)
        inputs: Iterable = iter(['y', '100', 'whatisthis', 'quit'])
        services.pay_taxes('water', input_method=lambda _: next(inputs))
        user_id: int = my_session.session.query(User).filter_by(name=username).first().id
        payment_id: int = my_session.session.query(Payment).filter_by(users_id=user_id).first().id

        assert isinstance(payment_id, int)

        services.edit_payment(payment_id, input_method=lambda _: next(inputs))
        captured_output = capsys.readouterr()
        coe: str = captured_output.out.strip()

        assert 'Selected payment is not found' not in coe
        assert 'ID' in coe
        assert 'Price' in coe
        assert 'Invalid option' in coe

    def test_payment_edit_details_value_error(self, my_session, capsys) -> None:
        username: str = 'checktaxessimple'
        password: str = 'StrongPass!'
        auth: Authorization = Authorization(engine=my_session, username=username, password=password, action='register')
        assert auth.user is not None
        services: Services = Services(auth.user, my_session)
        inputs: Iterable = iter([
            'y', '100', '1', '1'] + ['lol', 'January', '1999']+ ['1', '28', 'nonmonth', '1999'] +
            ['1', '28', '1', 'myyear'] + ['q', 'q'
        ])
        services.pay_taxes('water', input_method=lambda _: next(inputs))
        user_id: int = my_session.session.query(User).filter_by(name=username).first().id
        payment_id: int = my_session.session.query(Payment).filter_by(users_id=user_id).first().id
        assert isinstance(payment_id, int)

        services.edit_payment(payment_id, input_method=lambda _: next(inputs))
        captured_output = capsys.readouterr()
        coe: str = captured_output.out.strip()
        our_payment: Payment = my_session.session.get(Payment, payment_id)
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

    def test_payment_edit_details_second_option_value_error(self, my_session, capsys) -> None:
        username: str = 'checktaxessimple'
        password: str = 'StrongPass!'
        auth: Authorization = Authorization(engine=my_session, username=username, password=password, action='register')
        assert auth.user is not None
        services: Services = Services(auth.user, my_session)
        inputs: Iterable = iter([
            'y', '100', '1', '2'] + ['lol']+ ['2', '11p'] +
            ['q', 'q'
        ])
        services.pay_taxes('water', input_method=lambda _: next(inputs))
        user_id: int = my_session.session.query(User).filter_by(name=username).first().id
        payment_id: int = my_session.session.query(Payment).filter_by(users_id=user_id).first().id
        assert isinstance(payment_id, int)

        services.edit_payment(payment_id, input_method=lambda _: next(inputs))
        captured_output = capsys.readouterr()
        coe: str = captured_output.out.strip()
        our_payment: Payment = my_session.session.get(Payment, payment_id)
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


    def test_payment_edit_details_third_option_value_error(self, my_session, capsys) -> None:
        username: str = 'checktaxessimple'
        password: str = 'StrongPass!'
        auth: Authorization = Authorization(engine=my_session, username=username, password=password, action='register')
        assert auth.user is not None
        services: Services = Services(auth.user, my_session)
        inputs: Iterable = iter([
            'y', '100', '1', '3'] + ['lol']+ ['3', '11p'] + ['3', '1111111111111111'] +
            ['q', 'q'
        ])
        services.pay_taxes('water', input_method=lambda _: next(inputs))
        user_id: int = my_session.session.query(User).filter_by(name=username).first().id
        payment_id: int = my_session.session.query(Payment).filter_by(users_id=user_id).first().id
        assert isinstance(payment_id, int)

        services.edit_payment(payment_id, input_method=lambda _: next(inputs))
        captured_output = capsys.readouterr()
        coe: str = captured_output.out.strip()
        our_payment: Payment = my_session.session.get(Payment, payment_id)
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

    def test_delete_not_exisitng_tax(self, my_session) -> None:
        username: str = 'checktaxessimple'
        password: str = 'StrongPass!'
        auth: Authorization = Authorization(engine=my_session, username=username, password=password, action='register')
        assert auth.user is not None
        services: Services = Services(auth.user, my_session)
        user: User | None = my_session.get_user(username=username)
        inputs: Iterable = iter(['Y'])
        assert user is not None
        taxname: str = 'this is not valid name'
        with pytest.raises(KeyError, match='Tax doesn\'t exist'):
            services.delete_tax(taxname=taxname, input_method=lambda _: next(inputs))
        assert not any(tax for tax in user.taxes if tax.taxname == taxname)

    def test_delete_not_existing_tax_by_id(self, my_session) -> None:
        username: str = 'checktaxessimple'
        password: str = 'StrongPass!'
        auth: Authorization = Authorization(engine=my_session, username=username, password=password, action='register')
        assert auth.user is not None
        services: Services = Services(auth.user, my_session)
        user: User | None = my_session.get_user(username=username)
        inputs: Iterable = iter(['Y'])
        assert user is not None
        tax_id: int = -1
        with pytest.raises(KeyError, match="Tax doesn't exist"):
            services.delete_tax(tax_id=tax_id, input_method=lambda _: next(inputs))
        assert not any(tax for tax in user.taxes if tax.id == tax_id)

    def test_edit_not_existent_tax(self, my_session) -> None:
        username: str = 'checktaxessimple'
        password: str = 'StrongPass!'
        auth: Authorization = Authorization(engine=my_session, username=username, password=password, action='register')
        assert auth.user is not None
        services: Services = Services(auth.user, my_session)
        user: User | None = my_session.get_user(username=username)
        assert user is not None
        taxname: str = 'this is not valid tax name'
        with pytest.raises(KeyError, match="Tax doesn't exist"):
            services.edit_tax(taxname=taxname)

        assert not any(tax for tax in user.taxes if tax.taxname == taxname)

    def test_edit_non_existent_tax_by_id(self, my_session, capsys) -> None:
        username: str = 'checktaxessimple'
        password: str = 'StrongPass!'
        auth: Authorization = Authorization(engine=my_session, username=username, password=password, action='register')
        assert auth.user is not None
        services: Services = Services(auth.user, my_session)
        user: User | None = my_session.get_user(username=username)
        assert user is not None
        tax_id: int = -1
        with pytest.raises(KeyError, match="Tax doesn't exist"):
            services.edit_tax(tax_id=tax_id)
        captured_output: str = capsys.readouterr().out.strip()
        my_session.get_user(username).taxes

        assert 'edited successfully' not in captured_output
