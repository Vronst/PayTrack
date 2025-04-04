from dotenv import load_dotenv


load_dotenv()


def list_of_taxes(path_to_file: str | None = None) -> list[str]:
    """
    Reads a list of taxes from a file or returns a default list if the file is not found.

    Args:
        path_to_file (str): The path to the directory containing the taxes file. Defaults to '/home/vronst/Programming/Rachunki/app/'.

    Returns:
        list[str]: A list of tax names.
    """
    taxes_list: list[str] = []
    if path_to_file:
        try:
            with open(path_to_file, 'r') as file:
                for line in file:
                    taxes_list.append(line.strip())
        except FileNotFoundError:
            print('File with list of taxes not found\nDefault taxes applied')
    if not taxes_list:
        return [
            'water',
            'electricity',
            'gas',
            'internet',
            'phone',
            'house_tax',
            'ac/oc',
            'trash',
            'nursery',
            'school',
        ]
    return taxes_list


def simple_logs(message: str, error: str | None = None, log_file: list[str] = ['default']) -> None:
    """
    Logs a message to specified log files.

    Args:
        message (str): The message to log.
        error (str, optional): An optional error message to log. Defaults to None.
        log_file (list[str], optional): A list of log file names to write the message to. Defaults to ['default'].

    Raises:
        ValueError: If the LOGS_PATH environment variable is not set.
    """
    import os
    print(f'{message} {error}' if error else message)
    path: str | None = os.getenv('LOGS_PATH', None)
    if not path:
        raise ValueError('PATH environment variable is not set')
    for file in log_file:
        with open(path + file, 'a+') as log:
            log.write(f'{message} {error}\n\n' if error else f'{message}\n\n')


class NameTaken(Exception):
    pass


class PasswordNotSafe(Exception):
    pass


class LoginError(Exception):
    pass


class UserCreationError(Exception):
    pass


