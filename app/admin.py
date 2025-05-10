from typing import Callable
from tabulate import tabulate
from werkzeug.security import generate_password_hash
from .database.engine import MyEngine
from .database.models import User, Payment, Tax
from .utils import LoginError, get_model_columns, convert_type
from .messages import admin_dict


class AdminServices:
    """
    Provides an interface for admin users to view and modify database entries.

    This class allows administrators to perform CRUD operations on User, Payment, 
    and Tax models through a CLI interface.

    Attributes:
        user (User): The currently authenticated admin user.
        engine (MyEngine): SQLAlchemy engine instance for database operations.
        input_method (Callable): Function for handling user input (default is built-in input).
        is_running (bool): Flag to control main loop execution.
        options (dict): Maps table names to their SQLAlchemy models and display headers.
        models (dict): Maps table names to their corresponding SQLAlchemy models.
    """

    options = {
        'tax': (
            Tax,
            ['Id', 'Tax name', 'Payment Status', 'User id']
        ),
        'payment': (
            Payment,
            ['Id', 'Price', 'Date', 'Tax id', 'User id']
        ),
        'user': (
            User,
            ['Id', 'Admin status', 'Name', 'Password']
        )
    } # :no-index:
    models = {'user': User, 'tax': Tax, 'payment': Payment} # :no-index:

    def __init__(self, admin_user: User, engine: MyEngine) -> None:
        """
        Initializes the AdminServices class with an admin user and database engine.

        Args:
            admin_user (User): The user attempting to access admin functionality.
            engine (MyEngine): The SQLAlchemy engine for database communication.

        Raises:
            LoginError: If the provided user is not an admin.
        """
        if not admin_user.admin:
            raise LoginError("You don't have admin privileges to access this")
        self.user = admin_user
        self.engine = engine

    def show_data(self, data: str, *, input_method: Callable = input, out_method: Callable = print) -> None:
        """
        Displays entries of a given table and provides options for CRUD operations.

        Args:
            data (str): The name of the model to access ('user', 'tax', or 'payment').
            input_method (Callable, optional): Function to capture user input. Defaults to built-in input().
            out_method (Callable, optional): A function that accepts a string and outputs it.
        """
        selected, headers = self.options[data]
        others = {
            'user': ['tax', 'payment'],
            'tax': ['user', 'payment'],
            'payment': ['tax', 'user']
        }

        while self.is_running:
            entries = self.engine.session.query(selected).all()
            rows = [[getattr(entry, col) for col in get_model_columns(selected)] for entry in entries]
            out_method(tabulate(rows, headers=headers))
            choice = input_method(admin_dict[data])
            match choice:
                case '1':
                    self.add_data(data, input_method=input_method)
                case '2':
                    self.edit_data(data, input_method=input_method)
                case '3':
                    self.delete_data(data, input_method=input_method)
                case '4':
                    selected, headers = self.options[others[data][0]]
                case '5':
                    selected, headers = self.options[others[data][1]]
                case 'exit':
                    self.is_running = False
                case 'q':
                    return
                case _:
                    out_method("Invalid choice")

    def edit_data(self, data: str, *, input_method: Callable = input, out_method: Callable = print) -> None:
        """
        Edits an existing entry in the database based on its ID.

        Args:
            data (str): The table name of the entry to edit.
            input_method (Callable, optional): Function to capture user input. Defaults to built-in input().
            out_method (Callable, optional): A function that accepts a string and outputs it.
        """
        model = self.models[data]
        fields = dict(enumerate(get_model_columns(model), 1))

        id_ = input_method("Id of entry you want to edit: ")
        try:
            selected_entry = self.engine.session.get(model, int(id_))
            if not selected_entry:
                raise KeyError("Invalid id")
        except (ValueError, KeyError) as e:
            out_method(f"Invalid id {e}")
            return

        while self.is_running:
            row = [[getattr(selected_entry, col) for col in get_model_columns(model)]]
            out_method(tabulate(row, headers=self.options[data][1]))

            for number, field in fields.items():
                out_method(f'{number}. Edit {field}')
            out_method("S. Save and exit\nq. Abandon")

            choice = input_method('\n').strip()
            if choice.lower() == 'q':
                self.engine.session.rollback()
                out_method("Abandoned changes")
                return
            elif choice.lower() == 'exit':
                self.engine.session.rollback()
                out_method("Abandoned changes")
                self.is_running = False
                return
            elif choice.upper() == 'S':
                self.engine.session.add(selected_entry)
                self.engine.session.commit()
                out_method("Successfully saved")
                return
            try:
                field = fields[int(choice)]
            except (ValueError, KeyError):
                out_method(f"Invalid choice {choice}")
            else:
                new = input_method(f"New value for {field}: ")
                try:
                    new = convert_type(model, field, new)
                except ValueError:
                    out_method(f"Invalid value for {field}")
                else:
                    setattr(selected_entry, field, new)

    def delete_data(self, data: str, *, input_method: Callable = input, out_method: Callable = print) -> None:
        """
        Deletes a database entry by its ID.

        Args:
            data (str): The table name of the entry to delete.
            input_method (Callable, optional): Function to capture user input. Defaults to built-in input().
            out_method (Callable, optional): A function that accepts a string and outputs it.
        """
        model = self.models[data]
        choice = input_method(f"Type ID of the {data} you want to delete: ")
        try:
            entry = self.engine.session.get(model, int(choice))
            if not entry:
                raise KeyError("Invalid id")
            confirm = input_method(f"Are you sure you want to delete {entry}? (Y/n): ")
            if confirm.strip().upper() == 'Y':
                self.engine.session.delete(entry)
                self.engine.session.commit()
                out_method("Successfully deleted")
            else:
                out_method("Abandoned")
        except Exception as e:
            out_method(f"Deletion failed due to: {e}")
            self.engine.session.rollback()

    def add_data(self, data: str, *, input_method: Callable = input, out_method: Callable = print) -> None:
        """
        Creates and adds a new entry to the specified table.

        Args:
            data (str): The table name where the new entry should be added.
            input_method (Callable, optional): Function to capture user input. Defaults to built-in input().
            out_method (Callable, optional): A function that accepts a string and outputs it.
        """
        model = self.models[data]
        fields = get_model_columns(model)
        result = {}

        for field in fields:
            if field.lower() == 'id':
                continue
            value = input_method(f'{field}: ')
            if field.lower() == 'password':
                value = generate_password_hash(value, salt_length=24)
            try:
                result[field] = convert_type(model, field, value)
            except ValueError:
                out_method(f"Invalid input for field '{field}'. Entry aborted.")
                return

        try:
            new = model(**result)
            out_method(new)
            if input_method("S. Save\nq. Abandon: ").strip().upper() == 'S':
                self.engine.session.add(new)
                self.engine.session.commit()
                out_method("Successfully saved")
            else:
                out_method("Abandoned")
        except Exception as e:
            out_method(f"Failed to add new {data} due to: {e}")
            self.engine.session.rollback()
