from typing import TYPE_CHECKING

import pytest
from paytrack.models.savings import Savings


if TYPE_CHECKING:
    from paytrack.models.user import User


class TestPositiveSavings:

    @pytest.mark.regression
    def test_included(self, session, users):
        currency_id: int = 1
        owner_id: int = 1

        savings: Savings = Savings(
            currency_id=currency_id,
            owner_id=owner_id
        )
        
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
        
