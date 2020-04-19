from typing import Iterable, List

import numpy
from mpmath import findroot
from numpy import linspace, array, ndarray

from src.solver.AbstractSolver import AbstractSolver, SOLUTION
from src.util import fill
from test_equpment.parameter.ComplexNumberParameter import ComplexNumberParameter
from test_equpment.solution.ApproximateTwoDimensionComplexVectorSolution import \
    ApproximateTwoDimensionComplexVectorSolution


class EquationSolver(AbstractSolver[ApproximateTwoDimensionComplexVectorSolution, ComplexNumberParameter]):
    def __init__(self, dimension: int, left_border: int, right_border: int, frequency: int):
        super().__init__()
        self._dimension = dimension
        self._left_border = left_border
        self._right_border = right_border
        self._frequency = frequency

    def problem(self, argument):
        def first(one: complex) -> complex:
            return self.generator(one, self.parameter.number)

        def second(two: complex) -> complex:
            return self.generator(two - 1 + 0j, self.parameter.number)

        return first(argument[0]), second(argument[1])

    @staticmethod
    def set_precision(precision: float):
        ApproximateTwoDimensionComplexVectorSolution.set_equal_round(precision)

    def solve(self) -> Iterable[SOLUTION]:
        grid: ndarray = self.__get_grid()
        solutions: List[ApproximateTwoDimensionComplexVectorSolution] = []

        for approx_point in grid:
            dirty_solution = findroot(
                lambda one, two: self.problem([one, two]),
                (approx_point[0], approx_point[1])
            )

            converted_dirty_solution = numpy.array(dirty_solution).astype(numpy.complex)
            solution = ApproximateTwoDimensionComplexVectorSolution(converted_dirty_solution.item(0),
                                                                    converted_dirty_solution.item(1))

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
