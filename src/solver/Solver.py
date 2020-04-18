from abc import ABC, abstractmethod
from typing import Callable, List, Iterable, Generic, TypeVar

from src.solution.Solution import Solution as AbstractSolution

Solution = TypeVar('Solution', bound=AbstractSolution)
Parameter = TypeVar('Parameter')


class Solver(ABC, Generic[Solution, Parameter]):
    def __init__(self, generator: Callable[[complex, Parameter], complex]) -> None:
        self.generator = generator

    @abstractmethod
    def set_parameter(self, parameter: Parameter):
        pass

    @abstractmethod
    def problem(self, argument: List[complex]) -> List[complex]:
        pass

    @abstractmethod
    def solve(self) -> List[Solution]:
        pass
