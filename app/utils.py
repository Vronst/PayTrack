from dotenv import load_dotenv


load_dotenv()


def list_of_taxes(path_to_file: str = '/home/vronst/Programming/Rachunki/app/') -> list[str]:
    """
    Reads a list of taxes from a file or returns a default list if the file is not found.

    Args:
        path_to_file (str): The path to the directory containing the taxes file. Defaults to '/home/vronst/Programming/Rachunki/app/'.

    Returns:
        list[str]: A list of tax names.
    """
    taxes_list: list[str] = []
    try:
        with open(path_to_file + 'taxes.txt', 'r') as file:
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


# taxes: list[str] = list_of_taxes() 


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


def update() -> None:
    """
    Updates the database with the current date.

    This function imports the necessary modules and updates the database with the current date. So the payments from last months won't count
    this month's taxes as paid.
    """
    import datetime
    from datetime import date
    from .database.models import Tax 
    
    today: date = datetime.date.today()
    month: int
    year: int
    
    def change_status(tax: Tax) -> None:
        tax.payment_status = False
        session.add(tax)
        session.commit()
        simple_logs(f'{tax.taxname} payment status changed ({today.month, today.year})', log_file=['taxes.log'])
    
    taxes: list[Tax] = session.query(Tax).filter_by(payment_status=True).all()
    for tax in taxes:
        if not tax.payments:
            change_status(tax)
            continue
        for payment in tax.payments:
            day, month, year = list(map(int, payment.date.split('-')))
            if (month < today.month and year <= today.year) or year < today.year:
                change_status(tax)
                continue


class NameTaken(Exception):
    pass


class PasswordNotSafe(Exception):
    pass


class LoginError(Exception):
    pass
