from abc import ABC, abstractmethod
from typing import Callable, List, Generic, TypeVar

from src.parameter.AbstaractParameter import AbstractParameter
from src.solution.AbstractSolution import AbstractSolution

SOLUTION = TypeVar('SOLUTION', bound=AbstractSolution)
PARAMETER = TypeVar('PARAMETER', bound=AbstractParameter)


class AbstractSolver(ABC, Generic[SOLUTION, PARAMETER]):
    def __init__(self) -> None:
        self.generator = None  # Should be set in the appropriate setter
        self.parameter = None  # Should be set in the appropriate setter

    def set_generator(self, generator: Callable[[complex, PARAMETER], complex]):
        self.generator = generator

    def set_parameter(self, parameter: PARAMETER):
        self.parameter = parameter

    @abstractmethod
    def problem(self, argument: List[complex]) -> List[complex]:
        pass

    @abstractmethod
    def solve(self) -> List[SOLUTION]:
        pass

