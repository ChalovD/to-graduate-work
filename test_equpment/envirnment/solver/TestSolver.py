from typing import Iterable, Callable, List

import numpy
from mpmath import findroot
from numpy import linspace, array, ndarray

from src.solver.Solver import Solver
from src.util import fill
from test_equpment.envirnment.solution.TestSolution import SolutionWithComplexMember
from test_equpment.envirnment.solution.TestSolution import TestSolution


class TestSolver(Solver[SolutionWithComplexMember, complex]):
    def __init__(self, generator: Callable[[complex, complex], complex], dimension: int, left_border: int,
                 right_border: int, frequency: int):
        super().__init__(generator)
        self._dimension = dimension
        self._left_border = left_border
        self._right_border = right_border
        self._frequency = frequency
        self._parameter = None

    def set_parameter(self, parameter: complex):
        self._parameter = parameter

    def problem(self, argument):
        def first(one: complex) -> complex:
            return self.generator(one, self._parameter)

        def second(two: complex) -> complex:
            return self.generator(two - 1 + 0j, self._parameter)

        return first(argument[0]), second(argument[1])

    @staticmethod
    def set_precision(precision: float):
        TestSolution.set_equal_round(precision)

    def solve(self) -> Iterable[SolutionWithComplexMember]:
        grid: ndarray = self.__get_grid()
        solutions: List[SolutionWithComplexMember] = []

        for approx_point in grid:
            dirty_solution = findroot(
                lambda one, two: self.problem([one, two]),
                (approx_point[0], approx_point[1])
            )

            converted_dirty_solution = numpy.array(dirty_solution).astype(numpy.complex)
            solution = TestSolution(converted_dirty_solution.item(0), converted_dirty_solution.item(1))

            if solution not in solutions:
                solutions.append(solution)

        return solutions

    def __get_grid(self) -> ndarray:
        basic_grid: ndarray = linspace(self._left_border, self._right_border, self._frequency)
        items = range(0, self._dimension)
        grid: ndarray = array([])

        for _ in items:
            grid = fill(grid, basic_grid)

        return grid
