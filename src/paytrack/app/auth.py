from typing import Callable
from werkzeug.security import check_password_hash
from . import User, MyEngine
from .services import Services
from .utils import NameTaken, PasswordNotSafe, LoginError


class Authorization:
    """
    Handles user authentication and session management.

    Provides functionality for login, logout, registration, and deleting user accounts. 
    Maintains the current user session and allows for guest sharing features.
    """

    _user: User | None
    _guest: list[int]
    _guest_list: list[int]
    services: Services | None

    def __init__(self, *, engine: MyEngine, action: str | None = None, **kwargs):
        """
        Initializes the Authorization class and optionally performs login or registration.

        Args:
            engine (MyEngine): Custom SQLAlchemy engine for database access.
            action (str, optional): Either 'login' or 'register' to immediately invoke that action.
            **kwargs: Arguments for the selected action (e.g., username, password).

        Raises:
            AttributeError: If engine is not a MyEngine instance.
        """
        self._user = None
        self._guest = []
        self._guest_list = []
        self._engine = engine
        self.services = None

        if not kwargs.get('test', False) and not isinstance(self._engine, MyEngine):
            raise AttributeError("Engine should be of type MyEngine")

        if action:
            eval(f'self.{action}("{kwargs.get("username")}", "{kwargs.get("password")}")')

    @property
    def engine(self) -> MyEngine:
        """
        Returns the database engine.

        Returns:
            MyEngine: The engine used to interact with the database.
        """
        return self._engine

    @engine.setter
    def engine(self, value) -> None:
        raise AttributeError("This attribute cannot be changed directly")

    @property
    def is_logged(self) -> bool:
        """
        Checks if a user is currently logged in.

        Returns:
            bool: True if a user is logged in, False otherwise.
        """
        return self._user is not None

    @property
    def guest(self) -> list[int]:
        """
        Returns the list of user IDs this user has granted guest access to.

        Returns:
            list[int]: List of user IDs with guest access.
        """
        return self._guest

    @property
    def guest_list(self) -> list[int]:
        """
        Returns the list of user IDs where the current user is a guest.

        Returns:
            list[int]: List of user IDs where the current user has guest access.
        """
        return self._guest_list

    @property
    def user(self) -> User | None:
        """
        Returns the currently logged-in user.

        Returns:
            User | None: The logged-in user, or None if no user is logged in.
        """
        return self._user

    @user.setter
    def user(self, *args) -> None:
        raise AttributeError("This attribute cannot be changed directly")

    def login(self, username: str, password: str) -> None:
        """
        Authenticates a user and starts a session.

        Args:
            username (str): Username to authenticate.
            password (str): Password for the given username.

        Raises:
            LoginError: If credentials are invalid or user is already logged in.
        """
        if not username or not password:
            raise LoginError("Username and password cannot be empty")

        if self._user:
            raise LoginError("Already logged in")

        selected_user: User | None = self._engine.get_user(username=username)
        if not isinstance(selected_user, User):
            raise LoginError("User doesn't exist")

        if check_password_hash(selected_user.password, password):
            self._user = selected_user
            self.services = Services(user=self._user, engine=self._engine)
        else:
            raise LoginError("Incorrect credentials")

    def logout(self) -> bool:
        """
        Logs out_method the currently logged-in user.

        Returns:
            bool: True if logout was successful, False if no user was logged in.
        """
        if self._user is None:
            return False

        self._user = None
        self._guest = []
        self._guest_list = []
        self.services = None
        return True

    def register(self, username: str, password: str, *, out_method: Callable = print) -> bool:
        """
        Registers a new user account.

        Args:
            username (str): Desired username (must not contain special characters or be reserved).
            password (str): Desired password (must be strong).
            out_method (Callable, optional): A function that accepts a string and outputs it.

        Raises:
            ValueError: If the username or password is invalid or account creation fails.
            NameTaken: If the username is already taken.
            PasswordNotSafe: If the password doesn't meet security requirements.

        Returns:
            bool: True if registration was successful.
        """
        if username in ('', 'test', 'admin', None, ' ') or any(x in username for x in '!@# $%^&*()+_}{":?><~`,./;\'[]-='):
            raise ValueError("Username cannot contain special characters")

        if self._user is not None:
            # maybe should be LoginError?
            #TODO: think about this
            out_method("Logout first")
            return False

        if self._engine.get_user(username):
            raise NameTaken("Username is already taken")

        if len(password) < 8:
            raise PasswordNotSafe("Password too short")

        if not any(x in password for x in "!@#$%^&*()?{}[]"):
            raise PasswordNotSafe("Password should contain at least one special character")

        if not any(char.isupper() for char in password):
            raise PasswordNotSafe("Password should contain at least one uppercase letter")

        if not any(char.islower() for char in password):
            raise PasswordNotSafe("Password should contain at least one lowercase letter")

        user: User | None = self._engine.create_user(username, password)
        if not user:
            raise ValueError("User creation failed")

        self._user = user
        self.services = Services(user=self._user, engine=self._engine)
        return True

    def delete_user(self, username: str, *, input_method: Callable = input, out_method: Callable = print) -> None:
        """
        Deletes a user account from the database.

        Only admins are allowed to delete accounts other than their own. Users can delete their own accounts.

        Args:
            username (str): Username of the account to delete.
            input_method (Callable, optional): Function to capture confirmation input. Defaults to built-in input().
            out_method (Callable, optional): A function that accepts a string and outputs it.

        Raises:
            LoginError: If the current user is not an admin.
            ValueError: If the user to delete is not found.
        """
        if self.user and not self.user.admin:
            raise LoginError("You must be logged in as an administrator to delete someone else's account.")

        user: User | None = self._engine.get_user(username=username)
        if not user:
            raise ValueError("User not found")

        out_method()
        confirm = input_method(
            f'Are you sure you want to delete account with ID={user.id}, username="{user.name}"? (Y/n): '
        )
        if confirm != 'Y':
            out_method("Abandoned action")
            return

        if self.user and self.user.name == username:
            confirm_self = input_method("Are you sure you want to delete your own account? (Y/n): ")
            if confirm_self != 'Y':
                out_method("Deleting your own account was cancelled")
                return
            else:
                self.logout()

        self._engine.session.delete(user)
        self._engine.session.commit()
        out_method(f'Account of "{username}" has been deleted')
