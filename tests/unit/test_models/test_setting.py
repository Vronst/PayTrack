import pytest  # noqa: D100
from sqlalchemy.exc import IntegrityError

from paytrack.models.setting import Setting


class TestPositiveSetting:  # noqa: D101
    def test_creation(self, session):  # noqa: D102
        user_id: int = 1
        setting: Setting = Setting(owner_id=user_id)

        session.add(setting)
        session.commit()

        assert setting.mode == "dark"
        assert setting.language_id == 1
        assert setting.owner_id == user_id


class TestNegativeSetting:  # noqa: D101
    def test_creation_no_owner(self, session):  # noqa: D102
        with pytest.raises(IntegrityError):
            setting: Setting = Setting()

            session.add(setting)
            session.commit()

    def test_incorrect_mode(self, session):  # noqa: D102
        user_id: int = 1
        mode = "not my type"

        with pytest.raises(ValueError):
            setting: Setting = Setting(owner_id=user_id, mode=mode)

            session.add(setting)
            session.commit()
