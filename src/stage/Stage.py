from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Type

from src.solution.Solution import Solution

SolutionOrSub = TypeVar('SolutionOrSub', bound=Solution)


class Stage(ABC, Generic[SolutionOrSub]):
    @abstractmethod
    def get_result(self, solution: SolutionOrSub) -> complex:
        pass
