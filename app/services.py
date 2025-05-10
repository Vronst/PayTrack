from typing import Callable, TYPE_CHECKING
import datetime
from datetime import date
from functools import wraps
from . import User, Tax, Payment
from .utils import LoginError, simple_logs
from .messages import payment_edit, edit_msg


if TYPE_CHECKING:
    from . import MyEngine
    from .auth import Authorization


class Services:
    """
    A service class for interacting with the tax and payment database.

    This class handles creation, editing, display, and deletion of taxes and 
    payments associated with a logged-in user. It also manages login verification.
    """
    # TODO: Maybe option to sync it to google sheets?

    def __init__(self, user: User, engine: "MyEngine") -> None:
        """
        Initialize Services with a user and a database engine.

        Args:
            user (User): Instance of User used to retrieve user-related records.
            engine (MyEngine): SQLAlchemy Engine instance tailored for the application.
        """
        self._user: User = user
        self._engine: "MyEngine" = engine

    @staticmethod
    def requires_login(func):
        """
        Decorator to enforce login.

        Raises:
            LoginError: If no valid User is assigned to the service.
        """
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not isinstance(self._user, User):
                raise LoginError("Before accessing services, log in")            
            return func(self, *args, **kwargs)
        return wrapper

    @property
    @requires_login
    def user(self) -> User:
        """
        Returns:
            User: The currently logged-in user.

        Raises:
            ValueError: If no user is logged in.
        """
        if self._user is None:
            raise ValueError('You must be logged in to use Services')
        return self._user

    @user.setter
    def user(self, value) -> None:
        """
        Prevents reassignment of the user attribute.

        Raises:
            AttributeError: Always raised to prevent user reassignment.
        """
        raise AttributeError("This attribute cannot be changed directly")

    @property
    def engine(self) -> "MyEngine":
        """
        Returns:
            MyEngine: The database engine currently in use.
        """
        return self._engine

    @engine.setter
    def engine(self, value) -> None:
        """
        Prevents reassignment of the engine attribute.

        Raises:
            AttributeError: Always raised to prevent engine reassignment.
        """
        raise AttributeError("This attribute cannot be changed directly")

    def check_taxes(self, simple: bool = False, *, out_method: Callable = print) -> dict[int, Tax]:
        """
        Display and return all taxes associated with the user.

        Args:
            simple (bool, optional): If True, displays taxes in a simplified format.
            out_method (Callable, optional): A function that accepts a string and outputs it.

        Returns:
            dict[int, Tax]: A dictionary of tax entries with index as key and Tax object as value.
        """
        # TODO: A way to see shared taxes

        result: dict = dict(enumerate(self.user.taxes))
        if simple:
            for number, tax in result.items():
                out_method(number, tax.taxname, sep=': ')
        else:
            out_method('Tax{:<12}| Is paid?{:<10}'.format('', ''))
            out_method('-' * 24)
            for number, tax in result.items():
                out_method(f'{number}) {tax.taxname:<15}| {str(tax.payment_status):<10}')
                out_method('-' * 24)

        return result

    def pay_taxes(self, tax: str, *, input_method: Callable = input, out_method: Callable = print) -> None:
        """
        Add a payment to an existing tax or create a new tax if it doesn't exist.

        Args:
            tax (str): The name of the tax.
            input_method (Callable, optional): Method for input collection. Defaults to built-in input().
            out_method (Callable, optional): A function that accepts a string and outputs it.
        """
        selected_tax: Tax | None

        if input_method(f'Is {tax} - correct (y/N)') != 'y':
            out_method('Aborted')
            return None

        price: float= float(input_method('Enter amount: '))
        date: str = datetime.date.today().strftime('%d-%m-%Y')
        selected_tax = self._engine.session.query(Tax).filter_by(taxname=tax, user_id=self.user.id).first()

        if not selected_tax:
            simple_logs(f'{tax} not found, attempting to add tax', log_file=['taxes.log'])
            selected_tax = Tax(
                taxname=tax,
                user_id=self.user.id
            )
            self._engine.session.add(selected_tax)
            self._engine.session.commit()

        payment: Payment = Payment(
            price=price,
            date=date,
            taxes_id=selected_tax.id,
            users_id=self.user.id
        )
        self._engine.session.add(payment)
        selected_tax.payment_status = True
        self._engine.session.add(selected_tax)
        self._engine.session.commit()
        simple_logs(f'{tax} paid successfully', log_file=['taxes.log'])
        return

    def view_payments(self, tax_name: str, *, input_method: Callable =input, out_method: Callable = print) -> None:
        """
        View and optionally edit payments related to a specific tax.

        Args:
            tax_name (str): Name of the tax to filter payments.
            input_method (Callable, optional): Method for input collection. Defaults to built-in input().
            out_method (Callable, optional): A function that accepts a string and outputs it.
        """
        selected_tax: Tax | None = self._engine.session.query(Tax).filter_by(
            taxname=tax_name, user_id=self.user.id).first()

        if not selected_tax:
            # out_method(f'{tax_name} not found')
            simple_logs(f'{tax_name} not found', log_file=['taxes.log'])
            return None
        payments: list[Payment] = self._engine.session.query(Payment).filter_by(users_id=self.user.id, taxes_id=selected_tax.id).all()
        out_method('')
        out_method('ID  |  Price  |  Date  |  Tax-name')
        for payment in payments:
            out_method(f'{payment.id})\t{payment.price}\t{payment.date}\t{payment.tax.taxname}')
        out_method('')
        choice: str = input_method("Press enter to continue or type id of payment you want to edit\n")
        if choice == '':
            return
        else:
            try:
                self.edit_payment(int(choice))
            except ValueError:
                out_method("Unknown choice")
            finally:
                return

    def edit_payment(self, payment_id: int, *, input_method=input, out_method: Callable = print) -> None:
        """
        View or modify a payment identified by its ID.

        Args:
            payment_id (int): The ID of the payment to be edited.
            input_method (Callable, optional): Method for input collection. Defaults to built-in input().
            out_method (Callable, optional): A function that accepts a string and outputs it.

        Raises:
            ValueError: If the payment with given ID is not found.
        
        """
        selected_payment: Payment | None = self._engine.session.query(Payment).filter_by(
            id=payment_id, users_id=self.user.id).first()
        if not selected_payment:
            raise ValueError("Selected payment is not found")
        choice: str
        while True:
            out_method('ID  |  Price  |  Date  |  Tax-name')
            out_method(f"{selected_payment.id})", selected_payment.price, selected_payment.date, selected_payment.tax.taxname, sep='\t')
            choice = input_method(payment_edit)
            match choice.lower():
                case '1':
                    try:
                        self.edit_details(selected_payment, input_method=input_method)
                    except ValueError as e:
                        out_method(e)
                case '2':
                    if input_method("Are you sure you want to delete this payment? (Y/n)\t") != 'Y':
                        out_method("Canceled")
                        break
                    self._engine.session.delete(selected_payment)
                    self._engine.session.commit()
                    out_method("Removed successfully")
                    return
                case value if value in ('q', 'quit'):
                    return
                case _:
                    out_method("Invalid option")
    
    def edit_details(self, chosen_payment: Payment, *, input_method=input, out_method: Callable = print) -> None:
        """ 
        Edit the fields of an existing payment.

        Args:
            chosen_payment (Payment): Payment object to be edited.
            input_method (Callable, optional): Method for input collection. Defaults to built-in input().
            out_method (Callable, optional): A function that accepts a string and outputs it.
        """
        while True:
            out_method('ID  |  Price  |  Date  |  Tax-name')
            out_method(f"{chosen_payment.id})", chosen_payment.price, chosen_payment.date, chosen_payment.tax.taxname, sep='\t')
            choice: str = input_method(edit_msg)
            match choice:
                case '1':
                    day: str | int = input_method("Day: ")
                    month: str | int = input_method("Month: ")
                    year: str = input_method("Full year (e.g. 2025): ")
                    try:
                        month = int(month)
                    except ValueError:
                        month_dict: dict = {
                            "January": 1,
                            "February": 2,
                            "March": 3,
                            "April": 4,
                            "May": 5,
                            "June": 6,
                            "July": 7,
                            "August": 8,
                            "September": 9,
                            "October": 10,
                            "November": 11,
                            "December": 12
                            }
                        try:
                            assert not isinstance(month, int)
                            month = month_dict[month.capitalize()]
                        except (KeyError, AssertionError):
                            out_method(f'This is not a month: {month}')
                            continue
                       
                    try:
                        day = int(day)
                        if (day > 28 and month == 2)\
                            or\
                            (day > 30 and month in (4, 6, 9, 11))\
                            or\
                            (day > 31):
                            raise ValueError(f'Tehre is no {day} in {month}')
                        date: str = f'{int(day):02d}-{month:02d}-{int(year)}'
                    except ValueError as e:
                        out_method(e)
                        continue
                    chosen_payment.date = date
                case '2':
                    try:
                        new_price: int = int(input_method("New price: "))
                    except ValueError as e:
                        out_method(e)
                        continue
                    chosen_payment.price = new_price
                case '3':
                    list_of_ids: list = self.user.taxes
                    ids_list: list = []
                    out_method('ID\t|Tax')
                    for taxes in list_of_ids:
                        out_method(taxes.id, taxes.taxname, sep='\t')
                        ids_list.append(taxes.id)
                    try:
                        selection: int = int(input_method("Select tax id: "))
                        if selection not in ids_list:
                            raise ValueError('Id out of range')
                    except ValueError as e:
                        out_method(f'Error occured:\n{e}')
                        continue
                    else:
                        chosen_payment.taxes_id = selection
                case '4':
                    if input_method("Are you sure you want to delete that payment? (Y/n)") == 'Y':
                        self._engine.session.delete(chosen_payment)
                        self._engine.session.commit()
                        out_method('Deleted successfully')
                        return
                    else:
                        out_method("Canceled\n")
                case value if value in ('q', 'quit'):
                    self._engine.session.add(chosen_payment)
                    self._engine.session.commit()
                    return
                case 'a':
                    self._engine.session.rollback()
                    out_method('Abandoned changes')
                    return
                case _:
                    out_method(f"Invalid choice {choice}")

    def edit_tax(self, taxname: str | None = None, tax_id: int | None = None, *, input_method=input, out_method: Callable = print) -> None:
        """ 
        Edit the name of an existing tax.

        Args:
            taxname (str | None, optional): The current name of the tax.
            tax_id (int | None, optional): The ID of the tax.
            input_method (Callable, optional): Method for input collection. Defaults to built-in input().
            out_method (Callable, optional): A function that accepts a string and outputs it.

        Raises:
            KeyError: If no matching tax is found.
        """
        tax: Tax | None 
        if tax_id:
            tax = self._engine.session.get(Tax, tax_id)
        else:
            tax = self._engine.session.query(Tax).filter_by(taxname=taxname, user_id=self.user.id).first()
        if not tax:
            raise KeyError("Tax doesn't exist")
        new_name: str = input_method("New tax name: ")
        if input_method(f"Are you sure, you want to change {tax.taxname} to {new_name} (y/n)") != 'y':
            out_method("Canceled")
            return
        tax.taxname, new_name = new_name, tax.taxname
        self._engine.session.add(tax)
        self._engine.session.commit()
        out_method(f"{new_name} -> {tax.taxname} edited successfully")
        return

    def delete_tax(self, taxname: str | None = None, tax_id: int | None = None, *, input_method=input, out_method: Callable = print) -> None:
        """  
        Delete a tax and all associated records.

        Args:
            taxname (str | None, optional): The name of the tax.
            tax_id (int | None, optional): The ID of the tax.
            input_method (Callable, optional): Method for input collection. Defaults to built-in input().
            out_method (Callable, optional): A function that accepts a string and outputs it.

        Raises:
            KeyError: If no matching tax is found.
        """
        tax: Tax | None
        if tax_id:
            tax = self._engine.session.get(Tax, tax_id)
        else:
            tax = self._engine.session.query(Tax).filter_by(taxname=taxname, user_id=self.user.id).first()
        if not tax:
            raise KeyError("Tax doesn't exist")
        if input_method(f"Are you sure, you wan't to delete {tax.taxname}? (y/n)").lower() != 'y':
            out_method("Canceled")
            return
            
        self._engine.session.delete(tax)
        self._engine.session.commit()
        out_method("Deleted successfully")
        return

    def add_tax(self, taxname: str, *, input_method=input, out_method: Callable = print) -> None:
        """
        Add a new tax entry for the user.

        Args:
            taxname (str): Name of the new tax to be added.
            input_method (Callable, optional): Method for input collection. Defaults to built-in input().
            out_method (Callable, optional): A function that accepts a string and outputs it.
        
        """
        if input_method(
            f"Are you sure, you want to create new tax: {taxname} (y/n)"
        ).lower() != 'y':
            out_method("Canceled")
            return
        
        new_tax: Tax = Tax(taxname=taxname, user_id=self.user.id)
        self._engine.session.add(new_tax)
        self._engine.session.commit()
        out_method("Tax added successfully")
        return

    def update(self) -> None:
        """ 
        Refresh tax payment statuses based on the current date.

        If a payment is outdated (from a previous month or year), the tax is marked unpaid.
        If a future-dated payment is found, the tax is marked as paid.
        
        """
        today: date = datetime.date.today()
        day: int
        month: int
        year: int
        
        def change_status(tax: Tax, to_what: bool = False) -> None:
            tax.payment_status = to_what
            self._engine.session.add(tax)
            self._engine.session.commit()
            simple_logs(f'{tax.taxname} payment status changed ({today.month, today.year})', log_file=['taxes.log'])
        
        taxes: list[Tax] = self._engine.session.query(Tax).filter_by(payment_status=True).all()
        for tax in taxes:
            if not tax.payments:
                change_status(tax)
                continue
            for payment in tax.payments:
                day, month, year = list(map(int, payment.date.split('-')))
                if (month < today.month and year <= today.year) or year < today.year:
                    change_status(tax)
                    continue

        taxes: list[Tax] = self._engine.session.query(Tax).filter_by(payment_status=False).all()
        for tax in taxes:
            for payment in tax.payments:
                day, month, year = list(map(int, payment.date.split('-')))
                if (month > today.month and year >= today.year) or year > today.year:
                    change_status(tax, to_what=True)
                    break


        
