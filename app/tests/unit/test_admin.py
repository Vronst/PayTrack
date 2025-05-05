from typing import Iterator
import pytest
from ...admin import AdminServices
from ...utils import LoginError


class TestAdminServicesPositive:
    
    def test_init_admin_user(self, admin_user, mock_engine) -> None:
        AdminServices(admin_user=admin_user, engine=mock_engine)

    def test_admin_show_data_taxes(self, admin_user, capsys, mock_engine) -> None:
        inputs: Iterator = iter(['exit'])
        admin: AdminServices = AdminServices(admin_user, mock_engine)
        admin.show_data(data='tax', input_method=lambda _: next(inputs))
        out: str = capsys.readouterr().out.strip()
        assert 'Tax name' in out
        assert 'Payment Status' in out

    class TestPaymentsData:
        @pytest.mark.regression
        def test_add_new_payment(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterator = iter(['111', '01-01-2024', '1', '1', 'S', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.add_data(data='payment', input_method=lambda _: next(inputs))
            out = capsys.readouterr().out.strip()
            assert 'Successfully saved' in out

        def test_admin_show_data_payments(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterator = iter(['exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.show_data(data='payment', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Price' in out 
            assert 'Date' in out

        def test_admin_edit_data_payments(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterator = iter(['1', 'S'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='payment', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Price' in out
            assert 'Successfully saved' in out

        @pytest.mark.regression
        def test_admin_payments_go_to_users(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterator = iter(['5', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.show_data(data='payment', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Price' in out
            assert 'Password' in out

        @pytest.mark.regression
        def test_admin_payments_go_to_taxes(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterator = iter(['4', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.show_data(data='payment', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Price' in out
            assert 'Payment Status' in out

        @pytest.mark.regression
        def test_admin_delete_payment(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterator = iter(['1', 'Y', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.delete_data(data='payment', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Successfully deleted' in out

        @pytest.mark.regression
        def test_admin_edit_data_payments_date(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterator = iter(['1', '3', '15-01-2025', 'S'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='payment', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Price' in out
            assert 'Invalid' not in out
            assert 'Successfully saved' in out

        @pytest.mark.regression
        def test_admin_edit_data_payments_date_abandon(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterator = iter(['1', '3', '15-01-2025', 'S'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='payment', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Invalid' not in out
            assert 'Abandon' in out

        @pytest.mark.regression
        def test_admin_edit_data_payments_price(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterator = iter(['1', '2', '100', 'S'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='payment', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Price' in out
            assert 'Successfully saved' in out
            
        def test_admin_edit_data_payments_price_abandon(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterator = iter(['1', '2', '100', 'q'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='payment', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Price' in out
            assert 'Abandon' in out

        @pytest.mark.regression
        def test_admin_edit_data_payments_tax_id(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterator = iter(['1', '4', '100', 'S'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='payment', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Price' in out
            assert 'Successfully saved' in out

        def test_admin_edit_data_payments_tax_id_abandon(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterator = iter(['1', '4', '100', 'q'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='payment', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Price' in out
            assert 'Abandoned' in out

        @pytest.mark.regression
        def test_admin_edit_data_payments_user_id(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterator = iter(['1', '5', '100', 'S'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='payment', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Price' in out
            assert 'Successfully saved' in out

        def test_admin_edit_data_payments_user_id_abandon(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterator = iter(['1', '5', '100', 'q'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='payment', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Price' in out
            assert 'Abandoned' in out
            
        @pytest.mark.regression
        def test_admin_edit_data_payments_id(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterator = iter(['1', '1', '100', 'S'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='payment', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Price' in out
            assert 'Successfully saved' in out

        def test_admin_edit_data_payments_id_abandon(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterator = iter(['1', '1', '100', 'q'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='payment', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Price' in out
            assert 'Abandoned' in out

    class TestUserData:
        def test_admin_show_data_users(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterator = iter(['exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.show_data(data='user', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Password' in out

        @pytest.mark.regression
        def test_add_new_user(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterator = iter(['false', 'newuser', 'password1', 'S', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.add_data(data='user', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Successfully saved' in out

        def test_add_new_user_abandon(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterator = iter(['false', 'newuser', 'password1', 'q', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.add_data(data='user', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Abandoned' in out
            assert 'Failed to add' not in out

        def test_admin_edit_data_users(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterator = iter(['1', 'S'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='user', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Password' in out
            assert 'Successfully saved' in out

        @pytest.mark.regression
        def test_admin_edit_data_users_id(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterator = iter(['1', '1', '100', 'S', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='user', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Password' in out
            assert 'Invalid' not in out
            assert "Successfully saved" in out

        def test_admin_edit_data_users_id_abandon(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterator = iter(['1', '1', '100', 'q', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='user', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Password' in out
            assert "Abandoned" in out

        def test_admin_edit_data_users_name(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterator = iter(['1', '3', 'Hornet', 'S', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='user', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Password' in out
            assert "Successfully saved" in out

        def test_admin_edit_data_users_name_abandon(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterator = iter(['1', '3', 'Hornet', 'q', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='user', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Password' in out
            assert "Abandoned" in out

        def test_admin_edit_data_users_password(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterator = iter(['1', '3', 'Hornet', 'S', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='user', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Password' in out
            assert "Successfully saved" in out

        def test_admin_edit_data_users_password_abandon(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterator = iter(['3', '4', 'Hornet', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='user', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Password' in out
            assert "Successfully saved" not in out
            assert 'Abandoned' in out

        @pytest.mark.regression
        def test_admin_edit_data_users_delete(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterator = iter(['1', 'Y', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.delete_data(data='user', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert "Successfully deleted" in out

        def test_admin_edit_data_users_delete_abandon(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterator = iter(['1', 'n', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.delete_data(data='user', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert "Abandon" in out


    class TestTaxData:
        @pytest.mark.regression
        def test_add_new_payment_new_tax(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterator = iter(['Wlololo', 'True', '1', 'S', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.add_data(data='tax', input_method=lambda _: next(inputs))
            out = capsys.readouterr().out.strip()
            assert 'Successfully saved' in out

        @pytest.mark.regression
        def test_add_new_payment_existing(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterator = iter(['water', 'True', '1', 'S', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.add_data(data='tax', input_method=lambda _: next(inputs))
            out = capsys.readouterr().out.strip()
            assert 'Successfully saved' in out

        def test_admin_edit_tax(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterator = iter(['1', 'S'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='tax', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Payment Status' in out
            assert 'Successfully saved' in out

        @pytest.mark.regression
        def test_admin_edit_tax_go_to_payments(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterator = iter(['5', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.show_data(data='tax', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Payment Status' in out
            
        @pytest.mark.regression
        def test_admin_edit_tax_go_to_users(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterator = iter(['4', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.show_data(data='tax', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Password' in out

        @pytest.mark.regression
        def test_admin_edit_tax_tax_id(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterator = iter(['1', '1', '1000', 'S', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='tax', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Payment Status' in out
            assert 'Successfully saved' in out

        def test_admin_edit_tax_user_id(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterator = iter(['4', '4', '12', 'S', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='tax', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Payment Status' in out
            assert 'Successfully saved' in out

        @pytest.mark.regression
        def test_admin_edit_tax_all_options(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterator = iter(['1', '2', 'newname1', '1', '1', '4', '3', 'False', 'S', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='tax', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Payment Status' in out
            assert admin.is_running == True
            assert 'Successfully saved' in out

        def test_admin_edit_tax_all_options_abandon(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterator = iter(['1', '2', 'newname1', '1', '1', '3', 'True', '4', '12', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='tax', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Payment Status' in out
            assert 'Successfully saved' not in out
            assert 'Abandoned' in out

        def test_admin_delete_tax(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterator = iter(['2', 'Y', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.delete_data(data='tax', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Successfully deleted' in out

        def test_admin_edit_tax_abandon(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterator = iter(['1', '2', 'newname', 'q', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='tax', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Payment Status' in out
            assert 'Abandoned changes' in out


class TestAdminServicesNegative:

    def test_init_normal_user(self, mock_engine) -> None:
        normal_user = mock_engine.create_user()
        with pytest.raises(LoginError, match="You don't have admin privilages to access this"):
             AdminServices(admin_user=normal_user, engine=mock_engine)

    class TestUserData:  
        def test_admin_edit_data_users_wrong_input(self, capsys, admin_user, mock_engine) -> None:
            inputs: Iterator = iter(['10000a0', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='user', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Password' not in out
            assert 'Invalid id' in out

        def test_admin_edit_data_users_wrong_id(self, capsys, admin_user, mock_engine) -> None:
            inputs: Iterator = iter(['1', '1', 'my_name_is', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='user', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Password' in out
            assert 'Invalid value' in out

        def test_admin_delete_user_wrong_input(self, capsys, admin_user, mock_engine) -> None:
            inputs: Iterator = iter(['1', 'my_name_is', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.delete_data(data='user', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Abandoned' in out

    class TestTaxesData:
        def test_admin_edit_tax_incorrect_input(self, admin_user, capsys, mock_engine) -> None:
            inputs: Iterator = iter(['1', '2', 'newname', '1', 'a', 'S', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='tax', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Payment Status' in out
            assert 'Invalid value' in out
            assert 'Successfully saved' in out

        def test_admin_show_data_taxes_wrong_input(self, admin_user, mock_engine, capsys) -> None:
            inputs: Iterator = iter(['lolololo', '123123124', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.show_data(data='tax', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Payment Status' in out


    class TestPaymentsData:
        def test_admin_show_data_payments_wrong_input(self, capsys, mock_engine, admin_user) -> None:
            inputs: Iterator = iter(['lolololo', '123123124', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.show_data(data='payment', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Price' in out
            assert 'Invalid choice' in out

        def test_admin_edit_data_payments_wrong_input(self, capsys, mock_engine, admin_user) -> None:
            inputs: Iterator = iter(['1', '123123124', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='payment', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Price' in out
            assert 'Invalid choice' in out

        def test_admin_delete_payment_improper_input(self, mock_engine, capsys, admin_user) -> None:
            inputs: Iterator = iter(['lolololo', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.delete_data(data='payment', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Deletion failed due to' in out

        @pytest.mark.regression
        def test_admin_edit_data_payment_date_not_date(self, mock_engine, capsys, admin_user) -> None:
            inputs: Iterator = iter(['1', '3', 'notdata', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='payment', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Price' in out
            assert 'Invalid value for date' in out

        def test_admin_edit_data_payment_price_not_price(self, mock_engine, capsys, admin_user) -> None:
            inputs: Iterator = iter(['1', '2', 'notdata', 'S', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='payment', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Price' in out
            assert 'Invalid value for price' in out

        def test_admin_edit_data_payment_tax_id_invalid(self, mock_engine, capsys, admin_user) -> None:
            inputs: Iterator = iter(['1', '1', 'notdata', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='payment', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Invalid value' in out

        def test_admin_edit_data_payments_user_id_invalid(self, mock_engine, capsys, admin_user) -> None:
            inputs: Iterator = iter(['1', '5', 'notdata', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='payment', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Invalid value' in out
            assert 'Saved' not in out

        def test_admin_edit_data_payments_id_invalid(self, mock_engine, capsys, admin_user) -> None:
            inputs: Iterator = iter(['notdata', 'exit'])
            admin: AdminServices = AdminServices(admin_user, mock_engine)
            admin.edit_data(data='payment', input_method=lambda _: next(inputs))
            out: str = capsys.readouterr().out.strip()
            assert 'Invalid id' in out


