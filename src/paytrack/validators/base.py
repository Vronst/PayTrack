from abc import ABC, abstractmethod
from typing import TypeVar, Generic


T = TypeVar("T")


class Validator(ABC, Generic[T]):

    @abstractmethod
    def __call__(self, key: str, value: T) -> T:
        pass

