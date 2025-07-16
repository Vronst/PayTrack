def validate_name_if_custom(name: str | None, custom: bool):
    if custom and not name:
        raise ValueError("Name for custom categories must be provided")
    elif not custom and name:
        raise ValueError("Name for non custom categories cannot be edited")
