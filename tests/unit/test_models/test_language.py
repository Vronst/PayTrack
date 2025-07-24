import pytest  # noqa: D100
from sqlalchemy.exc import IntegrityError

from paytrack.models.language import Language


class TestPositiveLanguage:  # noqa: D101
    def test_creation(self, session):  # noqa: D102
        name: str = "Polski"
        code: str = "PL"
        language: Language = Language(language_name=name, language_code=code)
        session.add(language)
        session.commit()

        assert language.language_code == code
        assert language.language_name == name


class TestNegativeLanguage:  # noqa: D101
    def test_creation_no_name(self, session):  # noqa: D102
        with pytest.raises(IntegrityError):
            language: Language = Language(language_code="PL")
            session.add(language)
            session.commit()

    def test_creation_no_code(self, session):  # noqa: D102
        with pytest.raises(IntegrityError):
            language: Language = Language(language_name="Polski")
            session.add(language)
            session.commit()

    def test_creation_nothing(self, session):  # noqa: D102
        with pytest.raises(IntegrityError):
            language: Language = Language()
            session.add(language)
            session.commit()

    def test_creation_too_long_code(self, session):  # noqa: D102
        code: str = "PL" * 2
        name: str = "Polski"
        with pytest.raises(ValueError):
            language: Language = Language(
                language_name=name, language_code=code
            )
            session.add(language)
            session.commit()

    def test_creation_too_long_name(self, session):  # noqa: D102
        code: str = "PL"
        name: str = "P" * 16
        with pytest.raises(ValueError):
            language: Language = Language(
                language_name=name, language_code=code
            )
            session.add(language)
            session.commit()
