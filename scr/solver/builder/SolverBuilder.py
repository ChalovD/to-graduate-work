from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Callable

from scr.solution.AbstractSolution import AbstractSolution
from scr.solver import AbstractSolver

Solution = TypeVar['Solution', AbstractSolution]
FROM = TypeVar['FROM']
TO = TypeVar['TO']


class SolverBuilder(ABC, Generic[Solution, FROM, TO]):
    @abstractmethod
    def set_generator(self, generator: Callable[[FROM], TO]) -> None:
        pass

    @abstractmethod
    def build_solver(self) -> AbstractSolver:
        pass
