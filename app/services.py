import datetime
from .database import MyEngine
from .database import User, Tax, Payment
from .auth import Authorization
from .utils import simple_logs


class Services:
    # TODO: Maybe option to sync it to google sheets?

    def __init__(self, auth: Authorization, engine: MyEngine) -> None:
        self._auth = auth
        self._engine = engine
        # if not self.engine.session:
        #     print("To avoid errors, session has been started")
        #     self._engine.create_my_session()

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

    def check_taxes(self, simple: bool = False) -> None:
        # TODO: A way to see shared taxes
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
        # don't worry about session being None, in innit of this class
        # if it wasn't already initialized, it is
        selected_tax = self._engine.session.query(Tax).filter_by(taxname=tax, user_id=user.id).first()

        if not selected_tax:
            simple_logs(f'{tax} not found, attempting to add tax', log_file=['taxes.log'])
            print(f'{tax} not found, adding new tax')
            selected_tax = Tax(
                taxname=tax,
                user_id=user.id
            )
            self._engine.session.add(selected_tax)
            self._engine.session.commit()

        payment: Payment = Payment(
            price=price,
            date=date,
            taxes_id=selected_tax.id,
            users_id=user.id
        )
        self._engine.session.add(payment)
        selected_tax.payment_status = True
        self._engine.session.add(selected_tax)
        self._engine.session.commit()
        simple_logs(f'{tax} paid successfully', log_file=['taxes.log'])
        return
