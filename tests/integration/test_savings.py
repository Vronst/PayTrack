from typing import TYPE_CHECKING  # noqa: D100

import pytest

from paytrack.models.savings import Savings

if TYPE_CHECKING:
    from paytrack.models.user import User


class TestPositiveSavings:  # noqa: D101
    @pytest.mark.regression
    def test_included(self, session, users):  # noqa: D102
        currency_id: int = 1
        owner_id: int = 1

        savings: Savings = Savings(currency_id=currency_id, owner_id=owner_id)

        session.add(savings)
        session.commit()

        assert savings.included == []

        u1: User = users[0]
        savings.included.append(u1)

        session.add(savings)
        session.commit()

        assert savings.included == [u1]
        assert u1.shared_savings == [savings]
        assert u1.savings is not None
