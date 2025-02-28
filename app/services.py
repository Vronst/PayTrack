import datetime
from .database import MyEngine
from .database import User, Tax, Payment
from .auth import Authorization
from .utils import simple_logs


class Services:
    # TODO: Maybe option to sync it to google sheets?

    def __init__(self, auth: Authorization, engine: MyEngine) -> None:
        self.auth = auth
        self.engine = engine

    def check_taxes(self, simple: bool = False) -> None:
        # TODO: A way to see shared taxes
        # FIXME: something is not right with this, tests shows it prints ''
        user: User | None = self.auth.user
        if not user:
            raise ValueError("User not logged in")
        if simple:
            for tax in user.taxes:
                print(tax.taxname)
        else:
            print('Tax{:<12}| Is paid?{:<10}'.format('', ''))
            print('-' * 24)
            for tax in user.taxes:
                print(f'{tax.taxname:<15}| {str(tax.payment_status):<10}')
                print('-' * 24)

    def pay_taxes(self, tax: str) -> None:
        user: User | None
        selected_tax: Tax | None
        if not (user := self.auth.user):
            raise ValueError("User not logged in")

        price: float= float(input('Enter amount: '))
        date: str = datetime.date.today().strftime('%d-%m-%Y')
        selected_tax = self.engine.session.query(Tax).filter_by(taxname=tax, user_id=user.id).first()

        if not selected_tax:
            simple_logs(f'{tax} not found, attempting to add tax', log_file=['taxes.log'])
            print(f'{tax} not found, adding new tax')
            selected_tax = Tax(
                taxname=tax,
                user_id=user.id
            )
            self.engine.session.add(selected_tax)
            self.engine.session.commit()

        payment: Payment = Payment(
            price=price,
            date=date,
            taxes_id=selected_tax.id,
            users_id=user.id
        )
        self.engine.session.add(payment)
        selected_tax.payment_status = True
        self.engine.session.add(selected_tax)
        self.engine.session.commit()
        simple_logs(f'{tax} paid successfully', log_file=['taxes.log'])
        return
