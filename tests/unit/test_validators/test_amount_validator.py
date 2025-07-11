import pytest
from paytrack.validators import AmountValidator


class TestPositiveAmountValidator:

    def test_no_limits(self):
        validator: AmountValidator = AmountValidator()
        key, value = 'test', 123

        validator(key, value)

    def test_max_limit_exclusive(self):
        validator: AmountValidator = AmountValidator(max_amount=124)
        key, value = 'test', 123

        validator(key, value)

    def test_max_limit_inclusive(self):
        validator: AmountValidator = AmountValidator(max_amount=123, exclusive=False)
        key, value = 'test', 123

        validator(key, value)

    def test_min_limit_inclusive(self):
        validator: AmountValidator = AmountValidator(min_amount=123, exclusive=False)
        key, value = 'test', 123

        validator(key, value)

    def test_min_limit_exclusive(self):
        validator: AmountValidator = AmountValidator(min_amount=122, exclusive=True)
        key, value = 'test', 123

        validator(key, value)

    @pytest.mark.regression
    def test_min_max_exclusive(self):
        validator: AmountValidator = AmountValidator(min_amount=122, max_amount=124, exclusive=True)
        key, value = 'test', 123

        validator(key, value)

    @pytest.mark.regression
    def test_min_max_inclusive1(self):
        validator: AmountValidator = AmountValidator(min_amount=122, max_amount=123, exclusive=False)
        key, value = 'test', 123

        validator(key, value)

    def test_min_max_inclusive2(self):
        validator: AmountValidator = AmountValidator(min_amount=122, max_amount=123, exclusive=False)
        key, value = 'test', 122

        validator(key, value)


class TestNegativeAmountValidator:

    def test_min_limit_exclusive(self):
        validator: AmountValidator = AmountValidator(min_amount=123)
        key, value = 'test', 123 

        with pytest.raises(ValueError):
            validator(key, value)

    def test_min_limit_inclusive(self):
        validator: AmountValidator = AmountValidator(min_amount=124)
        key, value = 'test', 123 

        with pytest.raises(ValueError):
            validator(key, value)

    def test_max_limit_exclusive(self):
        validator: AmountValidator = AmountValidator(max_amount=123)
        key, value = 'test', 123 

        with pytest.raises(ValueError):
            validator(key, value)

    def test_max_limit_inclusive(self):
        validator: AmountValidator = AmountValidator(max_amount=123)
        key, value = 'test', 124 

        with pytest.raises(ValueError):
            validator(key, value)
