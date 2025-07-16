def validate_receiver(
    receiver_name: str | None, receiver_id: int | None
) -> None:
    if receiver_name and receiver_id:
        raise ValueError(
            "Receiver name cannot be set\
            on transaction when receiver_id is used"
        )
    elif not receiver_name and not receiver_id:
        raise ValueError(
            "Receiver name must be set, when not using receiver_id"
        )
