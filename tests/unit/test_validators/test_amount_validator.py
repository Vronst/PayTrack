import pytest  # noqa: D100

from paytrack.validators import AmountValidator


class TestPositiveAmountValidator:  # noqa: D101
    def test_no_limits(self):  # noqa: D102
        validator: AmountValidator = AmountValidator()
        key, value = "test", 123

        validator(key, value)

    def test_max_limit_exclusive(self):  # noqa: D102
        validator: AmountValidator = AmountValidator(max_amount=124)
        key, value = "test", 123

        validator(key, value)

    def test_max_limit_inclusive(self):  # noqa: D102
        validator: AmountValidator = AmountValidator(
            max_amount=123, exclusive=False
        )
        key, value = "test", 123

        validator(key, value)

    def test_min_limit_inclusive(self):  # noqa: D102
        validator: AmountValidator = AmountValidator(
            min_amount=123, exclusive=False
        )
        key, value = "test", 123

        validator(key, value)

    def test_min_limit_exclusive(self):  # noqa: D102
        validator: AmountValidator = AmountValidator(
            min_amount=122, exclusive=True
        )
        key, value = "test", 123

        validator(key, value)

    @pytest.mark.regression
    def test_min_max_exclusive(self):  # noqa: D102
        validator: AmountValidator = AmountValidator(
            min_amount=122, max_amount=124, exclusive=True
        )
        key, value = "test", 123

        validator(key, value)

    @pytest.mark.regression
    def test_min_max_inclusive1(self):  # noqa: D102
        validator: AmountValidator = AmountValidator(
            min_amount=122, max_amount=123, exclusive=False
        )
        key, value = "test", 123

        validator(key, value)

    def test_min_max_inclusive2(self):  # noqa: D102
        validator: AmountValidator = AmountValidator(
            min_amount=122, max_amount=123, exclusive=False
        )
        key, value = "test", 122

        validator(key, value)


class TestNegativeAmountValidator:  # noqa: D101
    def test_min_limit_exclusive(self):  # noqa: D102
        validator: AmountValidator = AmountValidator(min_amount=123)
        key, value = "test", 123

        with pytest.raises(ValueError):
            validator(key, value)

    def test_min_limit_inclusive(self):  # noqa: D102
        validator: AmountValidator = AmountValidator(min_amount=124)
        key, value = "test", 123

        with pytest.raises(ValueError):
            validator(key, value)

    def test_max_limit_exclusive(self):  # noqa: D102
        validator: AmountValidator = AmountValidator(max_amount=123)
        key, value = "test", 123

        with pytest.raises(ValueError):
            validator(key, value)

    def test_max_limit_inclusive(self):  # noqa: D102
        validator: AmountValidator = AmountValidator(max_amount=123)
        key, value = "test", 124

        with pytest.raises(ValueError):
            validator(key, value)
