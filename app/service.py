from .database.models import User, Payment, Tax
from .utils import simple_logs, taxes, update
from .database import session


def select_user(name: str) -> User | None:
    return session.query(User).filter_by(name=name).first()


def create_user(name: str, password: str) -> User | None:
    if session.query(User).filter_by(name=name).first():
        simple_logs('User already exists', log_file=['user.log'])
        print('User already exists')
        return None
    user = User(name=name, password=password)
    session.add(user)
    session.commit()
    for tax in taxes:
        tx: Tax = Tax(taxname=tax, user_id=user.id)
        user.taxes.append(tx)
    session.commit()
    simple_logs(f'User {name} created', log_file=['user.log'])
    return user


def check_taxes(user: User) -> None:
    print('Tax{:<12}| Is paid?{:<10}'.format('', ''))
    print('-' * 24)
    for tax in user.taxes:
        print(f'{tax.taxname:<15}| {str(tax.payment_status):<10}')
        print('-' * 24)


def pay_taxes(user: User, tax: str) -> None:
    import datetime
    price: float= float(input('Enter price: '))
    date: str = datetime.date.today().strftime('%d-%m-%Y')
    selected_tax: Tax | None = session.query(Tax).filter_by(taxname=tax, user_id=user.id).first()
    if not selected_tax:
        simple_logs(f'{tax} not found', log_file=['taxes.log'])
        print(f'{tax} not found')
        return
    # user.taxes.filter_by(taxname=tax).update({'payment_status': True})
    payment: Payment = Payment(
        price=price,
        date=date,
        taxes_id=selected_tax.id,
        users_id=user.id
    )
    session.add(payment)
    selected_tax.payment_status = True
    session.add(selected_tax)
    session.commit()
    simple_logs(f'{tax} paid successfully', log_file=['taxes.log'])
    return

    
def view_payments(user: User, tax: str) -> None:
    selected_tax: Tax | None = session.query(Tax).filter_by(taxname=tax, user_id=user.id).first()
    if not selected_tax:
        print(f'{tax} not found')
        simple_logs(f'{tax} not found', log_file=['taxes.log'])
        return None
    payments: list[Payment] = session.query(Payment).filter_by(users_id=user.id, taxes_id=selected_tax.id).all()
    print('')
    print('ID  |  Price  |  Date')
    for payment in payments:
        print(f'{payment.id})\t{payment.price}\t{payment.date}')
    print('')
    return


def edit_payment(user: User) -> None:
    while True:
        try:
            py_id: int = int(input('Enter payment id (q to quit): '))
        except ValueError:
            print('Exiting')
            return
        payment: Payment | None = session.query(Payment).filter_by(id=py_id, users_id=user.id).first()
        if not payment:
            print('Payment not found')
            simple_logs(f'Payment with id {py_id} of user {user.name} not found', log_file=['taxes.log'])
            return
        
        while True:
            print(payment)
            message: str = '''
                1. Edit price
                2. Edit date
                3. Delete payment
                q. Quit and save
                '''
            choice: str = input(message).lower()
            match choice:
                case '1':
                    price: float = float(input('Enter new price: '))
                    payment.price = price
                case '2':
                    # date: str = input('Enter new date (dd-mm-YYYY): ')
                    day: str = input('Enter day: ')
                    month: str = input('Enter month: ')
                    year: str = input('Enter year: ')
                    payment.date = day + '-' + month + '-' + year
                case '3':
                    session.delete(payment)
                    session.commit()
                    update()
                    break
                case 'q':
                    session.add(payment)
                    session.commit()
                    break
                case _:
                    print('Invalid choice')