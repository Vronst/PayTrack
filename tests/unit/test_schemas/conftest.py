import pytest  # noqa: D100


def skip_test(field: str, skip: list[str]) -> None:
    """Skips test with pytest.skip, if field is found in skip list.

    Arga:
        field (str): name of field to be checked against skip list.
        skip (list[str]): list of fields to be skipped.

    Returns:
        None
    """
    if field in skip:
        pytest.skip("Field not used in test")
