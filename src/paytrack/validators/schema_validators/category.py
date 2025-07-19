"""Validator used for validating category schema field: name/custom."""


def validate_name_if_custom(name: str | None, custom: bool):
    """Checks if ```name and custom``` are provided.

    If custom is True, name should be provided, else name is forbiden.

    Args:
        name (str | None): value of field with same name.

        custom (bool): value of field with same name.

    Raises:
        ValueError: If name is not None and custom is False, and reverse.
    """
    if custom and not name:
        raise ValueError("Name for custom categories must be provided")
    elif not custom and name:
        raise ValueError("Name for non custom categories cannot be edited")
