from getpass import getpass
from .auth import Authorization
from . import MyEngine, Tax, User
from .messages import (
        start_app as sam,
        check_taxes as ctl,
        inner_loop,
)
from .utils import LoginError, NameTaken, PasswordNotSafe


class TextApp:
    is_running: bool = False
    engine: MyEngine
    auth: Authorization
    debug: bool = False

    def start_app(self, debug: bool = False) -> None:
        self.is_running = True
        self._engine = MyEngine()
        self._engine.create_my_session()
        self.auth = Authorization(engine=self._engine)

        if debug:
            self.debug =True
            self.activate_debug_account()

        self.main_loop()

    def activate_debug_account(self):
        if not self._engine.create_user(username='test', password='test'):
            raise ValueError("Name already taken")
        print("Test account created")

    def close_app(self) -> None:
        self.is_running = False
        if self.debug:
            user: User | None = self._engine.session.query(User).filter_by(name='test').first()
            self._engine.session.delete(user)
            self._engine.session.commit()
            print("Test account deleted")
        self._engine.close_session()

        
    def main_loop(self) -> None:
        choice: str
        username: str
        password: str
        re_password: str

        while self.is_running:
            choice = input(sam)

            match choice:
                case '1':
                    username = input("Username: ")
                    password = getpass("Password: ") 
                    try:
                        self.auth.login(username, password)
                    except LoginError as e:
                        print(e)
                    else:
                        self.after_login()
                case '2':
                    username = input("Username: ")
                    while True:
                        password = getpass("Password: ")
                        re_password = getpass("Repeat password: ")
                        if password == re_password:
                            try:
                                self.auth.register(username, password)
                            except NameTaken as e:
                                print(e)
                                break
                            except PasswordNotSafe as e:
                                print(e)
                            else:
                                break
                        else:
                            print("Password does not match")
                    if self.auth.user:
                        self.after_login()
                case 'q':
                    self.close_app()
                case 'exit':
                    self.close_app()
                case _:
                    print('Unknown option')

    def after_login(self) -> None:
        # self.services = Services(auth=self.auth, engine=self._engine)

        while self.is_running:
            self.auth.services.update()
            choice: str = input(inner_loop)
            match choice:
                case '1':
                    self.check_taxes_loop()
                case '2':   
                    self.pay_taxes_loop()
                case 'q':
                    self.auth.logout()
                    return 
                case "exit":
                    self.close_app()
                case _:
                    print("Unknown option")

    def check_taxes_loop(self) -> None:
        """
            Allows to see payments associated with selected tax
        """
        while self.is_running:
            self.auth.services.update()
            tax_list: dict[int, Tax] = self.auth.services.check_taxes()
            choice: str = input(ctl)
            
            match choice:

                case value if any(tax.taxname.startswith(value) for tax in tax_list.values()):
                    full_name: str = next(tax.taxname for tax in tax_list.values() if tax.taxname.startswith(value))
                    self.auth.services.view_payments(full_name)
                case value if (value in str(tax_list)):
                    self.auth.services.view_payments(tax_list[int(value)].taxname)
                case 'q':
                    return None
                case 'exit':
                    self.close_app()
                case _:
                    print('Unknown option')

    def pay_taxes_loop(self) -> None:
        tax_list: dict[int, Tax] | None = None
        while self.is_running:
            ims: str = "Tax name to pay (or command): "
            tax: str | int = input(ims)
            if tax == 'help':
                print('Possible comands: help, q, exit')
                tax_list = self.auth.services.check_taxes(simple=True)
                tax = input(ims)
            try:
                tax = int(tax)
            except ValueError:
                pass
            else:
                if tax_list and tax in tax_list.keys():
                    self.auth.services.pay_taxes(tax_list[tax].taxname)
            if tax == 'q':
                return
            elif tax == 'exit':
                self.close_app()
            else:
                if isinstance(tax, str):
                    self.auth.services.pay_taxes(tax)
        self.auth.services.update()
