from abc import ABC, abstractmethod
from typing import Callable, List, Iterable, Generic, TypeVar

from src.solution.Solution import Solution as AbstractSolution

Solution = TypeVar('Solution', bound=AbstractSolution)


class Solver(ABC, Generic[Solution]):
    def _register(self, problem: Callable[[List[complex]], List[complex]]) -> None:
        self.problem = problem

    @abstractmethod
    def solve(self) -> List[Solution]:
        pass
