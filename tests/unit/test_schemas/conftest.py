import pytest 


def skip_test(field: str, skip: list):
    if field in skip:
        pytest.skip("Field not used in test")
