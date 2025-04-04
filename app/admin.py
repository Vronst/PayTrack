from typing import Callable
from .database.engine import MyEngine
from .database.models import User
from .utils import LoginError


class AdminServices:
    user: User
    engine: MyEngine
    input_method: Callable

    def __init__(self, admin_user: User, engine: MyEngine) -> None:
        if not admin_user.admin:
            raise LoginError("You don't have admin privilages to access this")
        self.user = admin_user
        self.engine = engine

    def show_data(self, *, input_method: Callable =input) -> None:
        pass

