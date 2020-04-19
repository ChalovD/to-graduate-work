from abc import ABC
from typing import Generic, TypeVar, Callable

from src.parameter.AbstaractParameter import AbstractParameter
from src.solution.AbstractSolution import AbstractSolution

SOLUTION = TypeVar('SOLUTION', bound=AbstractSolution)
PARAMETER = TypeVar('PARAMETER', bound=AbstractParameter)


class AbstractStage(ABC, Generic[SOLUTION, PARAMETER]):
    def __init__(self):
        self.generator = None  # Should be set in the appropriate setter
        self.parameter = None  # Should be set in the appropriate setter before use

    def set_generator(self, generator: Callable[[complex, PARAMETER], complex]):
        self.generator = generator

    def get_result(self, solution: SOLUTION) -> complex:
        pass

    def set_parameter(self, parameter: PARAMETER):
        self.parameter = parameter
