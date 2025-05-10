from typing import TypeVar, Callable, Type
from dotenv import load_dotenv
from sqlalchemy import Integer, Boolean, Float
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.inspection import inspect
from datetime import datetime


T = TypeVar("T", bound=DeclarativeBase)


load_dotenv()


def get_model_columns(model: Type[T]) -> list[str]:
    """
    Returns list of kolumns of the selected model.

    Args:
        model (Type[T]): A class that inherits from Base.

    Returns:
        list of str: List of column names
    """

    return [column.key for column in inspect(model).mapper.column_attrs]


def convert_type(model: Type[T], field: str, value: int | str, *, out_method: Callable = print) -> str | float | int:
    """
        Automatically converts type of value to given field of the model.

        Args:
            model (Type(T)): A class that inherits from Base.
            field (str): Field of selected model, that type will be checked.
            value (int or str): Value that we want to cast into type of selected field.
            out_method (Callable, optional): A function that accepts a string and outputs it.

        Returns:
            str | float | int: Same param casted for suitable type.
    """
    column_type = model.__table__.columns[field].type
    try:
        if isinstance(column_type, Integer):
            return int(value)
        elif isinstance(column_type, Boolean):
            assert isinstance(value, str)
            return value.lower() in ('true', '1', 'yes', 'y')
        elif isinstance(column_type, Float):
            return float(value)
        elif field == 'date':
            assert isinstance(value, str)
            datetime.strptime(value, '%d-%m-%Y')
            return value
        elif 'id' in field:
            return int(value)
    except ValueError:
        out_method(f"Invalid value for {field}")
        raise
    return value


def list_of_taxes(path_to_file: str | None = None, *, out_method: Callable = print) -> list[str]:
    """
    Reads a list of taxes from a file or returns a default list if the file is not found.

    Args:
        path_to_file (str): The path to the directory containing the taxes file. Defaults to '/home/vronst/Programming/Rachunki/app/'.
        out_method (Callable, optional): A function that accepts a string and outputs it.

    Returns:
        list of str: A list of tax names.
    """
    taxes_list: list[str] = []
    if path_to_file:
        try:
            with open(path_to_file, 'r') as file:
                for line in file:
                    taxes_list.append(line.strip())
        except FileNotFoundError:
            out_method('File with list of taxes not found\nDefault taxes applied')
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


def simple_logs(message: str, error: str | None = None, log_file: list[str] = ['default'], *, out_method: Callable = print) -> None:
    """
    Logs a message to specified log files.

    Args:
        message (str): The message to log.
        error (str, optional): An optional error message to log. Defaults to None.
        log_file (list of str, optional): A list of log file names to write the message to. Defaults to ['default'].
        out_method (Callable, optional): A function that accepts a string and outputs it.

    Raises:
        ValueError: If the LOGS_PATH environment variable is not set.
    """
    import os
    out_method(f'{message} {error}' if error else message)
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


