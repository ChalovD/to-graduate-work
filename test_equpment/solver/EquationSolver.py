import logging
from typing import Iterable, List

import numpy
from mpmath import findroot
from numpy import linspace, array, ndarray
from scipy.optimize import fsolve
from sympy import Symbol, lambdify, nsolve

from scr.main import FORMULAS
from scr.parameter.IonizationSymbols import IonizationSymbols
from scr.solver.AbstractSolver import AbstractSolver, SOLUTION
from scr.util import fill, restore_function, store_function, Number
from test_equpment.parameter.ComplexNumberParameter import ComplexNumberParameter
from test_equpment.solution.ApproximateTwoDimensionComplexVectorSolution import \
    ApproximateTwoDimensionComplexVectorSolution


class EquationSolver(AbstractSolver[ApproximateTwoDimensionComplexVectorSolution, ComplexNumberParameter]):
    def problem(self, argument: List[Number]) -> List[Number]:
        pass

    STORAGE1 = FORMULAS.joinpath('test-equation1')
    STORAGE2 = FORMULAS.joinpath('test-equation2')

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    def __init__(self, dimension: int, left_border: int, right_border: int, frequency: int):
        super().__init__()
        self.x = Symbol('x')
        self.y = Symbol('y')
        self.equation1 = self.get_analytic_equation1()
        self.equation2 = self.get_analytic_equation2()
        self.callable_equation1 = self.get_callable_equation1()
        self.callable_equation2 = self.get_callable_equation2()

        self._dimension = dimension
        self._left_border = left_border
        self._right_border = right_border
        self._frequency = frequency

    def second_eq(self, one1: Number, two2: Number) -> Number:
        return self.callable_equation2(one1, two2,
                                       self.parameter.T_d,
                                       self.parameter.F,
                                       self.parameter.omega_1,
                                       self.parameter.omega_2,
                                       self.parameter.etta_1,
                                       self.parameter.etta_2,
                                       self.parameter.N_1,
                                       self.parameter.N_2,
                                       self.parameter.f_0,
                                       self.parameter.I_p,
                                       self.parameter.p,
                                       self.parameter.p_theta
                                       )

    def first_eq(self, one1: Number, two1: Number) -> Number:
        return self.callable_equation1(one1, two1,
                                       self.parameter.T_d,
                                       self.parameter.F,
                                       self.parameter.omega_1,
                                       self.parameter.omega_2,
                                       self.parameter.etta_1,
                                       self.parameter.etta_2,
                                       self.parameter.N_1,
                                       self.parameter.N_2,
                                       self.parameter.f_0,
                                       self.parameter.I_p,
                                       self.parameter.p,
                                       self.parameter.p_theta
                                       )

    @staticmethod
    def set_precision(precision: float):
        ApproximateTwoDimensionComplexVectorSolution.set_equal_round(precision)

    def solve(self) -> Iterable[SOLUTION]:
        grid: ndarray = self.__get_grid()
        solutions: List[ApproximateTwoDimensionComplexVectorSolution] = []

        for approx_point in grid:
            try:
                dirty_solution = nsolve(
                    (self.first_eq(self.x, self.y), self.second_eq(self.x, self.y)),
                    (self.x, self.y),
                    (approx_point[0], approx_point[1])
                )

                converted_dirty_solution = numpy.array(dirty_solution).astype(numpy.complex)
                solution = ApproximateTwoDimensionComplexVectorSolution(converted_dirty_solution.item(0),
                                                                        converted_dirty_solution.item(1))

                print(self.first_eq(converted_dirty_solution.item(0), converted_dirty_solution.item(1)))
                print(self.second_eq(converted_dirty_solution.item(0), converted_dirty_solution.item(1)))
                print('next')

                if solution not in solutions:
                    solutions.append(solution)

            except (ValueError, ArithmeticError) as e:
                print(f"The error: {e} occurred")

        return solutions

    def get_callable_equation1(self):
        return lambdify((self.x, self.y,
                         IonizationSymbols.T_d,
                         IonizationSymbols.F,
                         IonizationSymbols.omega_1,
                         IonizationSymbols.omega_2,
                         IonizationSymbols.etta_1,
                         IonizationSymbols.etta_2,
                         IonizationSymbols.N_1,
                         IonizationSymbols.N_2,
                         IonizationSymbols.f_0,
                         IonizationSymbols.I_p,
                         IonizationSymbols.p,
                         IonizationSymbols.p_theta
                         ),
                        self.equation1
                        )

    def get_callable_equation2(self):
        return lambdify((self.x, self.y,
                         IonizationSymbols.T_d,
                         IonizationSymbols.F,
                         IonizationSymbols.omega_1,
                         IonizationSymbols.omega_2,
                         IonizationSymbols.etta_1,
                         IonizationSymbols.etta_2,
                         IonizationSymbols.N_1,
                         IonizationSymbols.N_2,
                         IonizationSymbols.f_0,
                         IonizationSymbols.I_p,
                         IonizationSymbols.p,
                         IonizationSymbols.p_theta
                         ),
                        self.equation2
                        )

    def get_analytic_equation1(self) -> Symbol:
        if self.STORAGE1.exists():
            return restore_function(self.STORAGE1)
        else:
            equation = self.first(self.x, self.y)
            store_function(self.STORAGE1, equation)
            return equation

    def first(self, t1: Symbol, t2: Symbol) -> Symbol:
        p = IonizationSymbols.T_d + IonizationSymbols.F + IonizationSymbols.omega_1 + IonizationSymbols.omega_2 + IonizationSymbols.etta_1 + IonizationSymbols.etta_2 + IonizationSymbols.N_1 + IonizationSymbols.N_2 + IonizationSymbols.f_0 + IonizationSymbols.I_p + IonizationSymbols.p + IonizationSymbols.p_theta

        return (t1 ** 2 + t2 ** 2 + p) * t1 * t2

    def get_analytic_equation2(self) -> Symbol:
        if self.STORAGE2.exists():
            return restore_function(self.STORAGE2)
        else:
            equation = self.second(self.x, self.y)
            store_function(self.STORAGE2, equation)
            return equation


    def second(self, t1: Symbol, t2: Symbol) -> Symbol:
        p = IonizationSymbols.T_d + IonizationSymbols.F + IonizationSymbols.omega_1 + IonizationSymbols.omega_2 + IonizationSymbols.etta_1 + IonizationSymbols.etta_2 + IonizationSymbols.N_1 + IonizationSymbols.N_2 + IonizationSymbols.f_0 + IonizationSymbols.I_p + IonizationSymbols.p + IonizationSymbols.p_theta

        return p * t1 + t2


    def __get_grid(self) -> ndarray:
        basic_grid: ndarray = linspace(self._left_border, self._right_border, self._frequency)
        items = range(0, self._dimension)
        grid: ndarray = array([])

        for _ in items:
            grid = fill(grid, basic_grid)

        return grid
