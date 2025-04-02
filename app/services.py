import datetime
from datetime import date
from functools import wraps
from .database import MyEngine
from .database import User, Tax, Payment
from .auth import Authorization
from .utils import LoginError, simple_logs
from .messages import payment_edit, edit_msg


class Services:
    # TODO: Maybe option to sync it to google sheets?

    def __init__(self, auth: Authorization, engine: MyEngine) -> None:
        self._auth: Authorization = auth
        self._engine: MyEngine = engine

    @staticmethod
    def requires_login(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            while (self._auth.user is None):
                print('You must log in to use services!')
                username: str = input('Username: ')
                password: str = input('Password: ')
                try:
                    self._auth.login(username, password)
                except LoginError as e:
                    print(e)
            return func(self, *args, **kwargs)
        return wrapper
            

    @property
    @requires_login
    def user(self) -> User:
        if self._auth.user is None:
            raise ValueError('You must be logged in to use Services')
        return self._auth.user

    @property
    def auth(self) -> Authorization:
        return self._auth

    @auth.setter
    def auth(self, value) -> None:
        raise AttributeError("This attribute cannot be changed directly")

    @property
    def engine(self) -> MyEngine:
        return self._engine

    @engine.setter
    def engine(self, value) -> None:
        raise AttributeError("This attribute cannot be changed directly")

    def check_taxes(self, simple: bool = False) -> dict[int, Tax]:
        # TODO: A way to see shared taxes

        result: dict = dict(enumerate(self.user.taxes))
        if simple:
            for number, tax in result.items():
                print(number, tax.taxname, sep=': ')
        else:
            print('Tax{:<12}| Is paid?{:<10}'.format('', ''))
            print('-' * 24)
            for number, tax in result.items():
                print(f'{number}) {tax.taxname:<15}| {str(tax.payment_status):<10}')
                print('-' * 24)

        return result

    def pay_taxes(self, tax: str) -> None:
        selected_tax: Tax | None

        if input(f'Is {tax} - correct (y/N)') != 'y':
            print('Aborted')
            return None

        price: float= float(input('Enter amount: '))
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

    def view_payments(self, tax_name: str) -> None:
        """
            Prints out payments associated with user and tax passed as variable
        """
        selected_tax: Tax | None = self._engine.session.query(Tax).filter_by(
            taxname=tax_name, user_id=self.user.id).first()

        if not selected_tax:
            # print(f'{tax_name} not found')
            simple_logs(f'{tax_name} not found', log_file=['taxes.log'])
            return None
        payments: list[Payment] = self._engine.session.query(Payment).filter_by(users_id=self.user.id, taxes_id=selected_tax.id).all()
        print('')
        print('ID  |  Price  |  Date  |  Tax-name')
        for payment in payments:
            print(f'{payment.id})\t{payment.price}\t{payment.date}\t{payment.tax.taxname}')
        print('')
        choice: str = input("Press enter to continue or type id of payment you want to edit\n")
        if choice == '':
            return
        else:
            try:
                self.edit_payment(int(choice))
            except ValueError:
                print("Unknown choice")
            finally:
                return

    def edit_payment(self, payment_id: int) -> None:
        selected_payment: Payment | None = self._engine.session.query(Payment).filter_by(
            id=payment_id, users_id=self.user.id).first()
        if not selected_payment:
            raise ValueError("Selected payment is not found")
        choice: str
        while True:
            print('ID  |  Price  |  Date  |  Tax-name')
            print(f"{selected_payment.id})", selected_payment.price, selected_payment.date, selected_payment.tax.taxname, sep='\t')
            choice = input(payment_edit)
            match choice.lower():
                case '1':
                    try:
                        self.edit_details(selected_payment)
                    except ValueError as e:
                        print(e)
                case '2':
                    if input("Are you sure you want to delete this payment? (Y/n)\t") != 'Y':
                        print("Canceled")
                        break
                    self._engine.session.delete(selected_payment)
                    self._engine.session.commit()
                    print("Removed successfully")
                    return
                case value if value in ('q', 'quit'):
                    return
                case _:
                    print("Invalid option")
    
    def edit_details(self, chosen_payment: Payment) -> None:
        while True:
            print('ID  |  Price  |  Date  |  Tax-name')
            print(f"{chosen_payment.id})", chosen_payment.price, chosen_payment.date, chosen_payment.tax.taxname, sep='\t')
            choice: str = input(edit_msg)
            match choice:
                case '1':
                    day: str | int = input("Day: ")
                    month: str | int = input("Month: ")
                    year: str = input("Full year (e.g. 2025): ")
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
                            month = month_dict[month.capitalize()]
                        except KeyError:
                            print(f'This is not a month: {month}')
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
                        print(e)
                        continue
                    chosen_payment.date = date
                case '2':
                    try:
                        new_price: int = int(input("New price: "))
                    except ValueError as e:
                        print(e)
                        continue
                    chosen_payment.price = new_price
                case '3':
                    list_of_ids: list = self.user.taxes
                    ids_list: list = []
                    print('ID\t|Tax')
                    for taxes in list_of_ids:
                        print(taxes.id, taxes.taxname, sep='\t')
                        ids_list.append(taxes.id)
                    try:
                        selection: int = int(input("Select tax id: "))
                        if selection not in ids_list:
                            raise ValueError('Id out of range')
                    except ValueError as e:
                        print(f'Error occured:\n{e}')
                        continue
                    else:
                        chosen_payment.taxes_id = selection
                case '4':
                    if input("Are you sure you want to delete that payment? (Y/n)") == 'Y':
                        self._engine.session.delete(chosen_payment)
                        self._engine.session.commit()
                        print('Deleted successfully')
                        return
                    else:
                        print("Canceled\n")
                case value if value in ('q', 'quit'):
                    self._engine.session.add(chosen_payment)
                    self._engine.session.commit()
                    return
                case 'a':
                    self._engine.session.rollback()
                    print('Abandoned changes')
                    return
                case _:
                    print(f"Invalid choice {choice}")

    def edit_tax(self, taxname: str | None = None, tax_id: int | None = None) -> None:
        tax: Tax | None 
        if tax_id:
            tax = self._engine.session.get(Tax, tax_id)
        else:
            tax = self._engine.session.query(Tax).filter_by(taxname=taxname, user_id=self.user.id).first()
        if not tax:
            raise KeyError("Tax doesn't exist")
        new_name: str = input("New tax name: ")
        if not input(f"Are you sure, you want to change {tax.taxname} to {new_name} (y/n)"):
            print("Canceled")
            return
        tax.taxname, new_name = new_name, tax.taxname
        self._engine.session.add(tax)
        self._engine.session.commit()
        print(f"{new_name} -> {tax.taxname} edited successfully")
        return

    def delete_tax(self, taxname: str | None = None, tax_id: int | None = None) -> None:
        tax: Tax | None
        if tax_id:
            tax = self._engine.session.get(Tax, tax_id)
        else:
            tax = self._engine.session.query(Tax).filter_by(taxname=taxname, user_id=self.user.id).first()
        if not tax:
            raise KeyError("Tax doesn't exist")
        if input(f"Are you sure, you wan't to delete {tax.taxname}? (y/n)").lower() != 'y':
            print("Canceled")
            return
            
        self._engine.session.delete(tax)
        self._engine.session.commit()
        print("Deleted successfully")
        return

    def add_tax(self, taxname: str) -> None:
        if input(
            f"Are you sure, you want to create new tax: {taxname} (y/n)"
        ).lower() != 'y':
            print("Canceled")
            return
        
        new_tax: Tax = Tax(taxname=taxname, user_id=self.user.id)
        self._engine.session.add(new_tax)
        self._engine.session.commit()
        print("Tax added successfully")
        return

    def update(self) -> None:
        """
        Updates the database with the current date.

        This function updates the database with the current date. So the payments from last months won't count
        this month's taxes as paid.
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


        
