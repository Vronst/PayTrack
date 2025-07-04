from abc import ABC, abstractmethod


class Validator[T](ABC):

    @abstractmethod
    def __call__(self, key: str, value: T) -> T:
        pass

