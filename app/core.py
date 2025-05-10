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
    Main class that initializes and runs the text-based tax application.
    """

    is_running: bool = False
    engine: MyEngine
    auth: Authorization
    debug: bool = False

    def start_app(self, *, input_method: Callable = input, debug: bool = False) -> None:
        """
        Starts the application by initializing the engine and authentication system.

        Args:
            input_method (Callable, optional): Function to handle user input, for mocking or testing. Defaults to input.
            debug (bool, optional): If True, connects to a test database. Defaults to False.

        Raises:
            RuntimeError: If the app is already running.
        """
        if self.is_running:
            raise RuntimeError("App is already running")

        if debug:
            self._engine = MyEngine(test=True, test_db="testtaxes")
            self._engine.create_my_session()
            assert self._engine.get_user(username="test") is None
            self._engine.create_user(username="test", password="test")
        else:
            self._engine = MyEngine()
            self._engine.create_my_session()

        self.is_running = True
        self.auth = Authorization(engine=self._engine)
        self.main_loop(input_method=input_method)

    def close_app(self) -> None:
        """
        Closes the application and releases all resources.
        """
        self.is_running = False
        self._engine.close_session()

    def main_loop(self, *, input_method: Callable = input) -> None:
        """
        Main user interaction loop before login.

        Args:
            input_method (Callable): Function to handle user input.
        """
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
                            print("Passwords do not match")
                    if self.auth.user:
                        self.after_login(input_method=input_method)

                case 'q' | 'exit':
                    self.close_app()

                case _:
                    print("Unknown option")

    def after_login(self, *, input_method: Callable = input) -> None:
        """
        Main user interaction loop after login.

        Args:
            input_method (Callable): Function to handle user input.
        """
        assert self.auth.user is not None
        assert self.auth.services is not None

        if self.auth.user.admin:
            while self.is_running:
                pass  # Placeholder for admin logic
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

                case 'exit':
                    self.close_app()

                case _:
                    print("Unknown option")

    def check_taxes_loop(self, *, input_method: Callable = input) -> None:
        """
        Allows the user to view payments associated with a selected tax.

        The user can search by tax name or prefix.

        Args:
            input_method (Callable): Function to handle user input.
        """
        assert self.auth.services is not None

        while self.is_running:
            self.auth.services.update()
            tax_list: dict[int, Tax] = self.auth.services.check_taxes()
            choice: str = input_method(ctl)

            match choice:
                case value if any(tax.taxname.startswith(value) for tax in tax_list.values()):
                    full_name: str = next(
                        tax.taxname for tax in tax_list.values() if tax.taxname.startswith(value)
                    )
                    self.auth.services.view_payments(full_name)

                case value if value.isdigit() and int(value) in tax_list:
                    self.auth.services.view_payments(tax_list[int(value)].taxname)

                case 'q':
                    return

                case 'exit':
                    self.close_app()

                case _:
                    print("Unknown option")

    def pay_taxes_loop(self, *, input_method: Callable = input) -> None:
        """
        Allows the user to make tax payments. Accepts tax name or ID.

        Commands:
            - 'help': Lists available taxes.
            - 'q': Returns to the previous menu.
            - 'exit': Closes the application.

        Args:
            input_method (Callable): Function to handle user input.
        """
        assert self.auth.services is not None
        tax_list: dict[int, Tax] | None = None

        while self.is_running:
            prompt = "Tax name to pay (or command): "
            tax: str = input_method(prompt)

            if tax == 'help':
                print("Possible commands: help, q, exit")
                tax_list = self.auth.services.check_taxes(simple=True)
                tax = input_method(prompt)

            try:
                tax_id = int(tax)
            except ValueError:
                tax_id = None

            if tax_id is not None and tax_list and tax_id in tax_list:
                self.auth.services.pay_taxes(tax_list[tax_id].taxname, input_method=input_method)
            elif tax == 'q':
                return
            elif tax == 'exit':
                self.close_app()
                return
            else:
                self.auth.services.pay_taxes(tax, input_method=input_method)

        self.auth.services.update()
