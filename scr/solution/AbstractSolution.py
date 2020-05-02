from abc import ABC
from typing import Generic, TypeVar

SOLUTION_KERNEL = TypeVar('SOLUTION_KERNEL')


class AbstractSolution(ABC, Generic[SOLUTION_KERNEL]):
    def get_solution(self) -> SOLUTION_KERNEL:
        pass

