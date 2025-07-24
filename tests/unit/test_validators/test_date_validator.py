from datetime import datetime, timedelta  # noqa: D100

import pytest

from paytrack.validators.date import DateValidator


class TestPositiveDateValidator:  # noqa: D101
    @pytest.mark.regression
    def test_date_dd_mm_yyyy(self):  # noqa: D102
        validator: DateValidator = DateValidator()
        key, value = "test", "20-10-2000"

        validator(key, value)

    @pytest.mark.regression
    def test_date_dd_mm_yy(self):  # noqa: D102
        validator: DateValidator = DateValidator()
        key, value = "test", "20-10-20"

        validator(key, value)

    def test_date_d_m_yy(self):  # noqa: D102
        validator: DateValidator = DateValidator()
        key, value = "test", "2-1-20"

        validator(key, value)

    @pytest.mark.regression
    def test_date_yyyy_m_d(self):  # noqa: D102
        validator: DateValidator = DateValidator()
        key, value = "test", "2000-1-2"

        validator(key, value)

    def test_past_date(self):  # noqa: D102
        validator: DateValidator = DateValidator(past_date=True)

        key, value = "test", datetime.now()

        validator(key, value)

    def test_past_date_set(self):  # noqa: D102
        validator: DateValidator = DateValidator(past_date=True)

        key, value = "test", "10-10-1999"

        validator(key, value)

    def test_future_date_set(self):  # noqa: D102
        validator: DateValidator = DateValidator(future_date=True)

        key, value = "test", "10-10-2999"

        validator(key, value)

    def test_future_date(self):  # noqa: D102
        validator: DateValidator = DateValidator(future_date=True)

        key, value = "test", datetime.now() + timedelta(days=1)

        validator(key, value)


class TestNegativeDateValidator:  # noqa: D101
    def test_date_with_letter(self):  # noqa: D102
        validator: DateValidator = DateValidator()
        key, value = "test", "2000-m1-10"

        with pytest.raises(ValueError):
            validator(key, value)

    def test_past_date(self):  # noqa: D102
        validator: DateValidator = DateValidator(past_date=True)

        key, value = "test", datetime.now() + timedelta(days=1, hours=1)

        with pytest.raises(ValueError):
            validator(key, value)

    @pytest.mark.regression
    def test_past_date_set(self):  # noqa: D102
        validator: DateValidator = DateValidator(past_date=True)

        key, value = "test", "10-10-2999"

        with pytest.raises(ValueError):
            validator(key, value)

    def test_future_date(self):  # noqa: D102
        validator: DateValidator = DateValidator(past_date=True)

        key, value = "test", datetime.now() - timedelta(days=1)

        validator(key, value)

    @pytest.mark.regression
    def test_future_date_set(self):  # noqa: D102
        validator: DateValidator = DateValidator(past_date=True)

        key, value = "test", "10-10-1999"

        validator(key, value)
