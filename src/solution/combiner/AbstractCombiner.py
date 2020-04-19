from abc import ABC, abstractmethod


class AbstractCombiner(ABC):
    @abstractmethod
    def combine(self, first: complex, second: complex) -> complex:
        pass

