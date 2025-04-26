from typing import Callable
from tabulate import tabulate
from werkzeug.security import generate_password_hash
from .database.engine import MyEngine
from .database.models import User, Payment, Tax
from .utils import LoginError, get_model_columns, convert_type
from .messages import admin_dict


class AdminServices:
    user: User
    engine: MyEngine
    input_method: Callable
    is_running: bool = True
    options: dict = {
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
        }

    def __init__(self, admin_user: User, engine: MyEngine) -> None:
        if not admin_user.admin:
            raise LoginError("You don't have admin privilages to access this")
        self.user = admin_user
        self.engine = engine

    def show_data(self, data: str, *, input_method: Callable = input) -> None:
        selected, headers = self.options[data]
        others = {
                'user': ['taxes', 'payment'],
                'tax': ['user', 'payment'],
                'payment': ['tax', 'user']
        }

        while self.is_running:
            entries = self.engine.session.query(selected).all()
            # print(headers)
            # for entry in entries:
            #     print(entry)
            print(tabulate(entries, headers=headers))
            choice = input_method(admin_dict[data])
            match choice:
                case '1':
                    # Add
                    self.add_data(data, input_method=input_method)
                case '2':
                    # Edit
                    self.edit_data(data, input_method=input_method)
                case '3':
                    # Delete
                    self.delete_data(data, input_method=input_method)
                case '4':
                    # Go to
                    selected, headers = self.options[others[data][0]]
                case '5':
                    # Go to
                    selected, headers = self.options[others[data][1]]
                case 'exit':
                    self.is_running = False
                case 'q':
                    return
                case _:
                    print("Invalid choice")

    def edit_data(self, data: str, *, input_method: Callable = input) -> None:
        choice: str
        models: dict = {'user': User, 'tax': Tax, 'payment': Payment}
        model = models[data]
        fields: dict = dict(enumerate(get_model_columns(model), 1))
    
        id_ = input_method("Id of entry you want to edit: ")
        try:
            selected_entry = self.engine.session.get(model, int(id_))
            if not selected_entry:
                raise KeyError("Invalid id")
        except (ValueError, KeyError) as e:
            print(f"Invalid id {e}")
            return

        while self.is_running:
            print(tabulate(selected_entry, headers=self.options[data][1]))
            for number, field in fields.items():
                print(f'{number}. Edit {field}')
            print(f"S. Save and exit\nq. Abandon")

            choice = input_method('\n')
            if choice == 'q':
                self.engine.session.rollback()
                print("Abandoned changes")
                return
            elif choice == 'exit':
                self.engine.session.rollback()
                print("Abandoned changes")
                self.is_running = False
                return
            elif choice == 'S':
                self.engine.session.add(selected_entry)
                self.engine.session.commit()
                print("Successfully saved")
                return
            try:
                field = fields[int(choice)]
            except (ValueError, KeyError):
                print(f"Invalid choice {choice}")
            else:
                new = input_method(f"New value for {field}: ")                
                try:
                    new = convert_type(model, field, new)
                except ValueError:
                    pass
                else:
                    setattr(selected_entry, field, new)

    def delete_data(self, data: str, *, input_method: Callable = input) -> None:
        option: dict = {
                'user': User,
                'payment': Payment,
                'tax': Tax
        }
        choice: str = input_method(f"Type id of {data} you want to delete: ")
        try:
            entry = self.engine.session.get(option[data], int(choice))
            if not entry:
                raise KeyError("Invalid id")
            choice = input_method(f"Are you sure you want to delete {entry}? (Y/n)")
            if choice == 'Y':
                self.engine.session.delete(entry)
                self.engine.session.commit()
                print("Successfully deleted")
            else:
                print("Abandoned")
        except Exception as e:
            print(f"Deletion failed due to: {e}")
            self.engine.session.rollback()


    def add_data(self, data: str, *, input_method: Callable = input) -> None:
        models = {'user': User, 'tax': Tax, 'payment': Payment}
        model = models[data]
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
                return

        try:
            new = model(**result)
            print(new)
            if input_method("S. Save\n q. Abandon") == 'S':
                self.engine.session.add(new)
                self.engine.session.commit()
                print("Successfully saved")
            else:
                print("Abandoned")
        except Exception as e:
            print(f"Failed to add new {data} due to: {e}")
            self.engine.session.rollback()

