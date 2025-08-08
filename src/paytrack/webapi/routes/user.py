"""Routes to interact with User table in database."""

from ...schemas import UserCreateSchema, UserReadSchema, UserUpdateSchema
from ...services.user import update_user_logic
from ..api import app


@app.post("/users/")
def create_user(user: UserCreateSchema):
    """Used to create user.

    Args:
        user (UserCreateSchema): User compatibile with UserCreateSchema.
    """
    return


@app.get("/users/")
def get_all_users():
    """Used to create user.

    Args:
        user (UserCreateSchema): User compatibile with UserCreateSchema.
    """
    result = UserReadSchema
    return


@app.get("/users/{user_id}")
def get_user(user_id: int):
    """Used to get user from database.

    Args:
        user_id (int): Id of selected user, passed in URL.
    """
    result = UserReadSchema
    return


@app.put("/users/{user_id}")
def update_user(user_data: UserUpdateSchema, user_id: int):
    """Used to replace user's data.

    Args:
        user_data (UserCreateSchema): User compatibile with UserCreateSchema.

        user_id (int): User's id passed in URL.

    Returns:
        `paytrack.services.user.update_user_logic`
    """
    return update_user_logic


@app.patch("/users/{user_id}")
def partialy_update_user(user_data: UserUpdateSchema, user_id: int):
    """Route to update partialy or fully user with patch method.

    Args:
        user_data (UserUpdateSchema): User data to be patched.

        user_id (int): Id of selected user, passed in URL.

    Returns:
        `paytrack.services.user.update_user_logic`
    """
    pass


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    """Used to delete user.

    Args:
        user_id (int): Id of user passed in URL.
    """
    return
