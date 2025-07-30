"""Base for all validators."""

from abc import ABC, abstractmethod


class Validator[T](ABC):
    """Abstract class blueprinting all validators."""

    @abstractmethod
    def __call__(self, key: str, value: T) -> T:
        """Abstract method.

        Should validate value.
        Key could be omitted.
        """
        pass

    def validate(self, value: T) -> T:
        """Validates value.

        Method that can be used instead of direct call,
        to implicitly omit key.
        """
        return self("Value", value)
