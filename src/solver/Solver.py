from abc import ABC, abstractmethod
from typing import Callable, List, Iterable, Generic, TypeVar

from src.solution.Solution import Solution

Solution = TypeVar['Solution', Solution]


class Solver(ABC, Generic[Solution]):
    @abstractmethod
    def __register(self, problem: Callable[[List[complex]], List[complex]]) -> None:
        pass

    @abstractmethod
    def solve(self) -> Iterable[Solution]:
        pass
