from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from src.solution import Solution
from src.solver import Solver

Solution = TypeVar['Solution', Solution]


class Consumer(ABC, Generic[Solution]):
    @abstractmethod
    def consume_by_solver(self, solver: Solver) -> complex:
        pass
