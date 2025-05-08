from getpass import getpass
from typing import Callable
from .auth import Authorization
from . import MyEngine, Tax
from .messages import (
        start_app as sam,
        check_taxes as ctl,
        inner_loop,
)
from .utils import LoginError, NameTaken, PasswordNotSafe


class TextApp:
    """
    Main class, that creates and uses the rest of class in this app.
    Takes no params on initiaton.
    """
    is_running: bool = False
    engine: MyEngine
    auth: Authorization
    debug: bool = False

    def start_app(self, *, input_method: Callable = input, debug: bool = False) -> None:
        """
        When used starts app, setting is_running on True. Creates engine (MyEngine) and choses default database or if debug is True test_db to connect to.

        Params:
        Callable: input_method - function responsible for providing users input or mocks
        Bool: debug - if true, choses connection with 'testtaxes' database.
        """
        if self.is_running:
            raise RuntimeError('App is already running')
        if debug:
            self._engine = MyEngine(test=True, test_db='testtaxes')
            self._engine.create_my_session()
            assert self._engine.get_user(username='test') is None
            self._engine.create_user(username='test', password='test')
            # self.activate_debug_account() not working and pointless?
        else:
            self._engine = MyEngine()
            self._engine.create_my_session()
        self.is_running = True
        self.auth = Authorization(engine=self._engine)


        self.main_loop(input_method=input_method)

    def close_app(self) -> None:
        """
        Sets is_running on False, closing app.
        Informs engine to drop connection and close session.
        """
        self.is_running = False
        self._engine.close_session()

        
    def main_loop(self, *, input_method: Callable = input) -> None:
        """Main loop (as in name)
            Params:
            Callable: input_method - function responsible for providing user inputs or mocks
        """
        choice: str
        username: str
        password: str
        re_password: str
        if input_method == input:
            gtpass = getpass
        else:
            gtpass = input_method

        while self.is_running:
            choice = input_method(sam)

            match choice:
                case '1':
                    username = input_method("Username: ")
                    password = gtpass("Password: ") 
                    try:
                        self.auth.login(username, password)
                    except LoginError as e:
                        print(e)
                    else:
                        self.after_login(input_method=input_method)
                case '2':
                    username = input_method("Username: ")
                    while True:
                        password = gtpass("Password: ")
                        re_password = gtpass("Repeat password: ")
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
                        self.after_login(input_method=input_method)
                case 'q':
                    self.close_app()
                case 'exit':
                    self.close_app()
                case _:
                    print('Unknown option')

    def after_login(self, *, input_method: Callable = input) -> None:
        """Should be used after successful login. Provides access for users to use services.

        Params:
        Callable: input_method - function responsible for providing user inputs or mocks
        """
        assert self.auth.user is not None
        assert self.auth.services is not None

        if self.auth.user.admin:
            while self.is_running:
                pass
            return

        while self.is_running:
            self.auth.services.update()
            choice: str = input_method(inner_loop)
            match choice:
                case '1':
                    self.check_taxes_loop(input_method=input_method)
                case '2':   
                    self.pay_taxes_loop(input_method=input_method)
                case 'q':
                    self.auth.logout()
                    return 
                case "exit":
                    self.close_app()
                case _:
                    print("Unknown option")

    def check_taxes_loop(self, *, input_method: Callable = input) -> None:
        """
            Allows to see payments associated with selected tax.
            Tax can be selected with starting letters due to .startswith() string method,
            or with fullname.

            Params:
            - Callable: input_method - function that will provide users inputs or mocks
        """
        assert self.auth.services is not None
        while self.is_running:
            self.auth.services.update()
            tax_list: dict[int, Tax] = self.auth.services.check_taxes()
            choice: str = input_method(ctl)
            
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

    def pay_taxes_loop(self, *, input_method: Callable = input) -> None:
        """Responsible for allowing user to add payments. Can also when 'help' inputed,
           will show existing taxes names

           Params:
           - Callable: input_method - function that will provide users inputs or mocks
        """

        assert self.auth.services is not None
        tax_list: dict[int, Tax] | None = None
        while self.is_running:
            ims: str = "Tax name to pay (or command): "
            tax: str | int = input_method(ims)
            if tax == 'help':
                print('Possible comands: help, q, exit')
                tax_list = self.auth.services.check_taxes(simple=True)
                tax = input_method(ims)
            try:
                tax = int(tax)
            except ValueError:
                pass
            else:
                if tax_list and tax in tax_list.keys():
                    self.auth.services.pay_taxes(tax_list[tax].taxname, input_method=input_method)
            if tax == 'q':
                return
            elif tax == 'exit':
                self.close_app()
                return
            else:
                if isinstance(tax, str):
                    self.auth.services.pay_taxes(tax, input_method=input_method)
        self.auth.services.update()
