from abc import ABC
from typing import Generic, TypeVar, Callable

from scr.parameter.AbstaractParameter import AbstractParameter
from scr.parameter.AbstractGeneratorParameter import AbstractGeneratorParameter
from scr.parameter.IonizationGeneratorParameter import IonizationGeneratorParameter
from scr.solution.AbstractSolution import AbstractSolution
from scr.util import Number

SOLUTION = TypeVar('SOLUTION', bound=AbstractSolution)
PARAMETER = TypeVar('PARAMETER', bound=AbstractParameter)


class AbstractStage(ABC, Generic[SOLUTION, PARAMETER]):
    def __init__(self, generator: Callable[[Number, AbstractGeneratorParameter], Number]):
        self.generator = generator
        self.parameter = None  # Should be set in the appropriate setter before use

    def get_result(self, solution: SOLUTION) -> Number:
        pass

    def set_parameter(self, parameter: PARAMETER):
        self.parameter = parameter
