#!/home/vronst/Programming/Rachunki/.venv/bin/python
from getpass import getpass
from sqlalchemy.orm import scoped_session
from app.database.models import User
from app.utils import simple_logs, taxes, update
from app import start_app, close_app
from app.service import (
    select_user,
    create_user,
    check_taxes,
    pay_taxes,
    view_payments,
    edit_payment,
)


def taxes_app() -> None:
    """
    Main application function for managing user taxes and payments.

    This function provides a command-line interface for users to create accounts,
    check their tax statuses, make payments, and view or edit payment details.
    """
    login_messege: str = '''
        1. Create a new user
        2. Choose a user
        q) Quit
        '''
    choice_messege: str = '''
        1. Check taxes
        2. Pay taxes
        q) Logout
        '''
    
    user: User | None = None
    name: str
    password: str

    update()
    while True:
        session: scoped_session = start_app()
        if not user:
            choice: str = input(login_messege)
            if choice == '1':
                name = input('Enter user name: ')
                password = getpass('Enter user password: ')
                user = create_user(name, password)
            elif choice == '2':
                user = select_user(input('Enter user name: '))
                password = getpass('Enter user password: ')
                if user and user.password == password:
                    simple_logs(f'User {user.name} logged in', log_file=['user.log'])
                else:
                    user = None
                    simple_logs('Invalid password or name', log_file=['user.log'])
            elif choice == 'q' or choice == 'exit':
                break
            else:
                print('Invalid choice')
                
        else:
            choice = input(choice_messege)
            if choice == '1':
                check_taxes_loop(user)
            elif choice == '2':
                tax: str = input('Enter tax name: ')
                pay_taxes(user, tax)
            elif choice == 'q' or choice == 'exit':
                user = None
            else:
                print('Invalid choice')
    close_app()
    print('Goodbye!')
    return


def check_taxes_loop(user: User) -> None:
    check_taxes_messege: str = '''
        1. Type name of tax to go into details 
        (example: "water")
        q) Quit
    '''
    while True:
        check_taxes(user)
        choice: str = input(check_taxes_messege).lower()
        match choice:
            case value if any(tax.startswith(value) for tax in taxes):
                full_tax_name = next(tax for tax in taxes if tax.startswith(value))
                pay_tax(user,full_tax_name)
            case 'q':
                break
            case _:
                continue
    return


def pay_tax(user: User, tax: str) -> None: 

    payment_messege: str = '''
        1. Pay {tx}
        2. View payments
        3. Edit payments by id
        q) Quit
        '''
    while True:
        choice: str = input(payment_messege.format(tx=tax)).lower()
        match choice:
            case '1':
                pay_taxes(user, tax)
            case '2':
                view_payments(user, tax)
            case '3':
                edit_payment(user)
            case 'q':
                break
            case _:
                continue

if __name__ == '__main__':
    import sys
    if '-N' in sys.argv:
        ...
    else:
        taxes_app()
