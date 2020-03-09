from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Callable

from src.solution.Solution import Solution
from src.solver import Solver

Solution = TypeVar['Solution', Solution]
FROM = TypeVar['FROM']
TO = TypeVar['TO']


class SolverBuilder(ABC, Generic[Solution, FROM, TO]):
    @abstractmethod
    def set_generator(self, generator: Callable[[FROM], TO]) -> None:
        pass

    @abstractmethod
    def build_solver(self) -> Solver:
        pass
