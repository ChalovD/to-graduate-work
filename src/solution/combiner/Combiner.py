from abc import ABC, abstractmethod


class Combiner(ABC):
    @abstractmethod
    def combine(self, first: complex, second: complex) -> complex:
        pass
