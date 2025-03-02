from getpass import getpass
from .auth import Authorization
from .database.engine import MyEngine
from .services import Services
from .messages import (
        start_app as sam,
)


class TextApp:
    is_running: bool = False
    engine: MyEngine
    auth: Authorization

    def start_app(self) -> None:
        self.is_running = True
        self._engine = MyEngine()
        self._engine.create_my_session()
        self.auth = Authorization(engine=self._engine)

        self.main_loop()

    def close_app(self) -> None:
        self.is_running = False
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
                    if self.auth.login(username, password):
                        self.after_login()
                case '2':
                    username = input("Username: ")
                    while True:
                        password = getpass("Password: ")
                        re_password = getpass("Repeat password: ")
                        if password == re_password and self.auth.register(username, password):
                            break
                        else:
                            print("Password does not match")
                    self.after_login()
                case 'q':
                    self.close_app()
                case 'exit':
                    self.close_app()
                case _:
                    print('Unknown option')

    def after_login(self) -> None:
        from .messages import inner_loop

        while self.is_running:
            choice: str = input(inner_loop)
            self.services = Services(auth=self.auth, engine=self._engine)

            match choice:
                case '1':
                    # TODO: Check taxes
                    self.services.check_taxes()       
                case '2':   
                    # TODO: Pay/Add taxes
                    self.services.check_taxes(simple=True)
                    tax: str = input("Tax name to pay: ")
                    if tax in ('q', 'exit'):
                        break
                    self.services.pay_taxes(tax)
                case 'q':
                    self.auth.logout()
                    break
                case "exit":
                    self.is_running = False
                case _:
                    print("Unknown option")

