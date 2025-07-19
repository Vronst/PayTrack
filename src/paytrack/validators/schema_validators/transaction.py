"""Validators for transaction schema."""


def validate_receiver(
    receiver_name: str | None, receiver_id: int | None
) -> None:
    """Validates if combo of name and receiver_id is valid.

    If receiver_id is present, name should not be provided.

    Args:
        receiver_name (str | None): value of field with same name.
        receiver_id (int | None): value of field with same name.

    Raises:
        ValueError: if both are not None.
    """
    if receiver_name and receiver_id:
        raise ValueError(
            "Receiver name cannot be set\
            on transaction when receiver_id is used"
        )
    elif not receiver_name and not receiver_id:
        raise ValueError(
            "Receiver name must be set, when not using receiver_id"
        )
