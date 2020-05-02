from abc import ABC, abstractmethod
from typing import Callable, List, Generic, TypeVar

from scr.parameter.AbstaractParameter import AbstractParameter
from scr.parameter.AbstractGeneratorParameter import AbstractGeneratorParameter
from scr.parameter.IonizationGeneratorParameter import IonizationGeneratorParameter
from scr.solution.AbstractSolution import AbstractSolution
from scr.util import Number

SOLUTION = TypeVar('SOLUTION', bound=AbstractSolution)
PARAMETER = TypeVar('PARAMETER', bound=AbstractParameter)


class AbstractSolver(ABC, Generic[SOLUTION, PARAMETER]):
    def __init__(self, generator: Callable[[Number, AbstractGeneratorParameter], Number]) -> None:
        self.generator = generator
        self.parameter = None  # Should be set in the appropriate setter

    def set_parameter(self, parameter: PARAMETER):
        self.parameter = parameter

    @abstractmethod
    def solve(self) -> List[SOLUTION]:
        pass

