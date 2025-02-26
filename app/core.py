from .messages import (
        start_app as sam,
)


class TextApp:
    __version__: str = '0.1.0'
    is_running: bool = False

    def start_app(self) -> None:
        self.is_running = True
        self.main_loop()

    def close_app(self) -> None:
        self.is_running = False
        
    def main_loop(self) -> None:
        choice: str

        while self.is_running:
            choice = input(sam)

            match choice:
                case '1':
                    ...
                case '2':
                    ...
                case 'q':
                    ...
                case 'exit':
                    self.close_app()
                case _:
                    print('Unknown option')


