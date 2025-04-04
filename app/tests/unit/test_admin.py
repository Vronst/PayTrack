from typing import Iterable
import pytest
from ...admin import AdminServices
from ...utils import LoginError


class TestAdminServicesPositive:
    
    def test_init_admin_user(self, admin_user, mock_engine) -> None:
        AdminServices(admin_user=admin_user, engine=mock_engine)

    def test_admin_show_data_taxes(self, admin_user, capsys, mock_engine) -> None:
        inputs: Iterable = iter(['exit'])
        admin: AdminServices = AdminServices(admin_user, mock_engine)
        admin.show_data(data='tax', input_method=lambda _: next(inputs))
        out: str = capsys.readouterr().out.strip()
        assert 'Tax id\t|\tUser id\t|\tUsername\t|\tTax name\t|\tPayment status' in out
        assert 'Add tax' in out
        assert 'Edit tax' in out
        assert 'Delete tax' in out
        assert 'Go to user' in out
        assert 'Go to payments' in out

    class TestPaymentsData:
        def test_admin_show_data_payments(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterable = iter(['exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.show_data(data='payment', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Payment id\t|\tUser id\t|\tUsername\t|\tTax id\t|\tPrice\t|\tDate' in out
            assert 'Add payment' in out
            assert 'Edit payment' in out
            assert 'Delete payment' in out
            assert 'Go to Tax' in out
            assert 'Go to User' in out

        def test_admin_edit_data_payments(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterable = iter(['exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='payment', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Payment id\t|\tUser id\t|\tUsername\t|\tTax id\t|\tPrice\t|\tDate' in out
            assert 'Edit id' in out
            assert 'Edit user id' in out
            assert 'Edit tax id' in out
            assert 'Edit price' in out
            assert 'Edit date' in out
            assert 'Delete it' in out
            assert 'Save and Quit' in out
            assert 'Abandon and Quit' in out
            assert 'Successfully saved' in out
            assert 'Go to users' in out
            assert 'Go to taxes' in out

        def test_admin_payments_go_to_users(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterable = iter(['3', '2', '10', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.show_data(data='payment', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Number of taxes' in out

        def test_admin_payments_go_to_taxes(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterable = iter(['3', '2', '11', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.show_data(data='payment', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Taxname' in out

        def test_admin_delete_payment(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterable = iter(['Y', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.delete_data(data='payment', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Successfully deleted' in out

        def test_admin_edit_payment_date(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterable = iter(['5', '2025-01-15', 's' 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='payment', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Successfully saved' in out

        def test_admin_edit_data_date_abandon(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterable = iter(['5', '2025-01-15', 's' 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='payment', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Abandon' in out

        def test_admin_edit_data_payments_price(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterable = iter(['4', '100', 's' 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='payment', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Successfully saved' in out
            
        def test_admin_edit_data_payments_price_abandon(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterable = iter(['4', '100', 'q' 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='payment', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Abandon' in out

        def test_admin_edit_data_payments_tax_id(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterable = iter(['3', '100', 's' 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='payment', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Successfully saved' in out

        def test_admin_edit_data_payments_tax_id_abandon(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterable = iter(['3', '100', 'q' 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='payment', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Abandoned' in out

        def test_admin_edit_data_payments_user_id(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterable = iter(['2', '100', 's' 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='payment', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Successfully saved' in out

        def test_admin_edit_data_payments_user_id_abandon(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterable = iter(['2', '100', 'q' 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='payment', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Abandon' in out
            
        def test_admin_edit_data_payments_id(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterable = iter(['1', '100', 's' 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='payment', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Successfully saved' in out

        def test_admin_edit_data_payments_id_abandon(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterable = iter(['1', '100', 'q' 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='payment', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Abandoned' in out

    class TestUserData:
        def test_admin_show_data_users(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterable = iter(['exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.show_data(data='user', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'User id\t|\tUsername\t|\tIs Admin\t|\tNumber of taxes\t|\tNumber of Payments' in out
            assert 'Add new user' in out
            assert 'Edit user' in out
            assert 'Go to Taxes' in out
            assert 'Go to Payments' in out

        def test_add_new_user(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterable = iter(['newuser', 'password1', 'S', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.add_data(data='user', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'successfully created' in out

        def test_add_new_user_abandon(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterable = iter(['newuser', 'password1', 'q', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.add_data(data='user', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Abandoned' in out

        def test_admin_edit_data_users(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterable = iter(['exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='user', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'User id\t|\tUsername\t|\tIs Admin\t|\tNumber of taxes\t|\tNumber of Payments' in out
            assert 'Edit id' in out
            assert 'Edit username' in out
            assert 'Edit password' in out
            assert 'Delete it' in out
            assert 'Save and Quit' in out
            assert 'Abandon and Quit' in out
            assert 'Successfully saved' in out
            assert 'Go to payments' in out
            assert 'Go to taxes' in out

        def test_admin_edit_data_users_id(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterable = iter(['1', '100', 'S', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='user', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert "Successfully saved" in out

        def test_admin_edit_data_users_id_abandon(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterable = iter(['1', '100', 'q', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='user', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert "Abandoned" in out

        def test_admin_edit_data_users_name(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterable = iter(['2', 'Hornet', 'S', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='user', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert "Successfully saved" in out

        def test_admin_edit_data_users_name_abandon(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterable = iter(['2', 'Hornet', 'q', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='user', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert "Abandoned" in out

        def test_admin_edit_data_users_password(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterable = iter(['3', 'Hornet', 'S', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='user', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert "Successfully saved" in out

        def test_admin_edit_data_users_password_abandon(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterable = iter(['3', 'Hornet', 'q', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='user', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert "Successfully saved" in out

        def test_admin_edit_data_users_delete(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterable = iter(['Y', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.delete_date(data='user', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert "Successfully deleted" in out

        def test_admin_edit_data_users_delete_abandon(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterable = iter(['n', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.delete_date(data='user', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert "Abandon" in out


    class TestTaxData:
        def test_admin_edit_tax(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterable = iter(['exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='tax', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Tax name\t|\tTax Id\t|\tUser id\t|\tUsername' in out
            assert 'Edit name' in out
            assert 'Edit Tax id' in out
            assert 'Edit User id' in out
            assert 'Delete it' in out
            assert 'Save and Quit' in out
            assert 'Abandon and Quit' in out
            assert 'Successfully saved' in out
            assert 'Go to users' in out
            assert 'Go to payments' in out

        def test_admin_edit_tax_go_to_payments(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterable = iter(['2', '9', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.show_data(data='tax', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Edit name' in out

        def test_admin_edit_tax_go_to_users(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterable = iter(['2', '8', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.show_data(data='tax', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Number of Payments' in out

        def test_admin_edit_tax_tax_id(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterable = iter(['2', '1000', 'S', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='tax', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Tax name\t|\tTax Id\t|\tUser id' in out
            assert 'Edit name' in out
            assert 'Edit Tax id' in out
            assert 'Edit User id' in out
            assert 'Delete it' in out
            assert 'Save and Quit' in out
            assert 'Abandon and Quit' in out
            assert 'Successfully saved' in out

        def test_admin_edit_tax_user_id(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterable = iter(['3', '1', 'S', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='tax', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Tax name\t|\tTax Id\t|\tUser id' in out
            assert 'Edit name' in out
            assert 'Edit Tax id' in out
            assert 'Edit User id' in out
            assert 'Delete it' in out
            assert 'Save and Quit' in out
            assert 'Abandon and Quit' in out
            assert 'Successfully saved' in out

        def test_admin_edit_tax_all_options(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterable = iter(['1', 'newname1', '2', '1', '3', '1', 'S', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='tax', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Tax name\t|\tTax Id\t|\tUser id' in out
            assert 'Edit name' in out
            assert 'Edit Tax id' in out
            assert 'Edit User id' in out
            assert 'Delete it' in out
            assert 'Save and Quit' in out
            assert 'Abandon and Quit' in out
            assert 'Successfully saved' in out

        def test_admin_edit_tax_all_options_abandon(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterable = iter(['1', 'newname1', '2', '1', '3', '1', 'q', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='tax', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Tax name\t|\tTax Id\t|\tUser id' in out
            assert 'Edit name' in out
            assert 'Edit Tax id' in out
            assert 'Edit User id' in out
            assert 'Delete it' in out
            assert 'Save and Quit' in out
            assert 'Abandon and Quit' in out
            assert 'Successfully saved' in out

        def test_admin_delete_tax(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterable = iter(['2', '2', '4', 'Y', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.delete_data(data='tax', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Tax name\t|\tTax Id\t|\tUser id' in out
            assert 'Edit name' in out
            assert 'Edit Tax id' in out
            assert 'Edit User id' in out
            assert 'Delete it' in out
            assert 'Save and Quit' in out
            assert 'Abandon and Quit' in out
            assert 'Are you sure you want to delete this?' in out
            assert 'Successfully deleted' in out

        def test_admin_edit_tax_abandon(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterable = iter(['1', 'newname', 'q', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='tax', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Tax name\t|\tTax Id\t|\tUser id' in out
            assert 'Edit name' in out
            assert 'Edit Tax id' in out
            assert 'Edit User id' in out
            assert 'Delete it' in out
            assert 'Save and Quit' in out
            assert 'Abandon and Quit' in out
            assert 'Abandoned changes' in out


class TestAdminServicesNegative:

    def test_init_normal_user(self, mock_engine) -> None:
        normal_user = mock_engine.create_user()
        with pytest.raises(LoginError, match="You don't have admin privilages to access this"):
             AdminServices(admin_user=normal_user, engine=mock_engine)

    class TestUserData:  
        def test_admin_

    class TestTaxesData:
        def test_admin_edit_tax_incorrect_input(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterable = iter(['2', 'newname', '1', 'S', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='tax', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Tax name\t|\tTax Id\t|\tUser id' in out
            assert 'Edit name' in out
            assert 'Edit Tax id' in out
            assert 'Edit User id' in out
            assert 'Delete it' in out
            assert 'Save and Quit' in out
            assert 'Abandon and Quit' in out
            assert 'Inccorect input' in out
            assert 'Successfully saved' in out

        def test_admin_show_data_taxes_wrong_input(self, admin_user, mock_engine, capsys) -> None:
            inputs: Iterable = iter(['lolololo', '123123124', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.show_data(data='tax', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Tax id' in out
            assert 'Add tax' in out
            assert 'Edit id' not in out

        def test_admin_

    class TestPaymentsData:
        def testa_admin_show_data_payments_wrong_input(self, capsys, mock_engine, admin_user) -> None:
            inputs: Iterable = iter(['lolololo', '123123124', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.show_data(data='payment', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'id' in out
            assert 'Add' in out
            assert 'Edit id' not in out
            assert 'Invalid option' in out

        def test_admin_edit_data_payments_wrong_input(self, capsys, mock_engine, admin_user) -> None:
            inputs: Iterable = iter(['lolololo', '123123124', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='payment', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'id' in out
            assert 'Add' in out
            assert 'Edit id' not in out
            assert 'Invalid option' in out

        def test_admin_delete_payment_inproper_input(self, mock_engine, capsys, admin_user) -> None:
            inputs: Iterable = iter(['lolololo', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.delete_data(data='payment', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Abandoned' in out

        def test_admin_edit_payment_date_not_date(self, mock_engine, capsys, admin_user) -> None:
            inputs: Iterable = iter(['5', 'notdata', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='payment', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Invalid date' in out

        def test_admin_edit_payment_price_not_price(self, mock_engine, capsys, admin_user) -> None:
            inputs: Iterable = iter(['4', 'notdata', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='payment', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Invalid price' in out

        def test_admin_edit_payment_tax_id_invalid(self, mock_engine, capsys, admin_user) -> None:
            inputs: Iterable = iter(['3', 'notdata', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='payment', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Invalid id' in out

        def test_admin_edit_payment_user_id_invalid(self, mock_engine, capsys, admin_user) -> None:
            inputs: Iterable = iter(['2', 'notdata', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='payment', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Invalid id' in out

        def test_admin_edit_payment_id_invalid(self, mock_engine, capsys, admin_user) -> None:
            inputs: Iterable = iter(['1', 'notdata', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='payment', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Invalid id' in out


