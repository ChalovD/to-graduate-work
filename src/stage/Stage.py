from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from src.solution.Solution import Solution

Solution = TypeVar['Solution', Solution]


class Stage(ABC, Generic[Solution]):
    @abstractmethod
    def get_result(self) -> complex:
        pass
