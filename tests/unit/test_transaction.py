from datetime import datetime
import pytest
from paytrack.models import Transaction


class TestPositiveTransaction:

    def test_creation(self, session, users) -> None:
        pass
        # user = users.pop(0)
        # t1 = Transaction(owner_id=user.id)

