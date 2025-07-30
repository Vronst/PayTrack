from copy import deepcopy  # noqa: D100

import pytest
from sqlalchemy.exc import IntegrityError

from paytrack.constants.setting import MODE_CHOICES
from paytrack.models.setting import Setting

params: list[dict] = [
    {
        "owner_id": 1,
        "mode": MODE_CHOICES[0],
    }
]

incorrect_types: list[tuple] = [
    ("owner_id", "owner_id"),
    ("mode", "inccorect_mode"),
    ("language_id", "language_id"),
]


@pytest.mark.parametrize("data", params)
class TestPositiveSetting:  # noqa: D101
    def test_creation(self, session, data):  # noqa: D102
        setting: Setting = Setting(**data)

        session.add(setting)
        session.commit()

        assert setting.mode == data["mode"]
        assert setting.language_id == 1
        assert setting.owner_id == data["owner_id"]


class TestNegativeSetting:  # noqa: D101
    def test_creation_no_owner(self, session):  # noqa: D102
        with pytest.raises(IntegrityError):
            setting: Setting = Setting()

            session.add(setting)
            session.commit()

    @pytest.mark.parametrize("data", params)
    @pytest.mark.parametrize("field, incorrect_data", incorrect_types)
    def test_incorrect_mode(self, session, data, field, incorrect_data):  # noqa: D102
        dt = deepcopy(data)
        dt[field] = incorrect_data

        with pytest.raises(ValueError):
            setting: Setting = Setting(**dt)

            session.add(setting)
            session.commit()
