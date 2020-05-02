import logging
from typing import Iterable, List, Callable

import numpy
from numpy import linspace, array, ndarray
from scipy.optimize import excitingmixing
from scipy.optimize.nonlin import NoConvergence, anderson, newton_krylov, diagbroyden, linearmixing
from sympy import Symbol, lambdify

from scr.calculation_equipment.Formulas import Formulas, diff_list, real_quad
from scr.main import FORMULAS, LOG_FILE, shared
from scr.parameter.IonizationGeneratorParameter import IonizationGeneratorParameter
from scr.parameter.IonizationParameter import IonizationParameter
from scr.parameter.IonizationSymbols import IonizationSymbols
from scr.solution.TwoValueSolution import TwoValueSolution
from scr.solver.AbstractSolver import AbstractSolver, SOLUTION
from scr.util import fill, Number, multiply, square, restore_function, store_function


class EquationSolver(AbstractSolver[TwoValueSolution, IonizationParameter]):
    STORAGE_1 = FORMULAS.joinpath('equation_1')
    STORAGE_2 = FORMULAS.joinpath('equation_2')

    def __init__(self,
                 generator: Callable[[Number, IonizationGeneratorParameter], Number],
                 dimension: int,
                 left_border: int,
                 right_border: int,
                 frequency: int
                 ) -> None:
        super().__init__(generator)
        self.logger = None
        self.set_up_logger()
        self.logger.debug(f"The generator {generator} is set")
        self.formulas = None
        self.init_formulas()
        self.logger.debug(f"Formulas for EquationSolver class initialized")
        self.x = Symbol('x')
        self.y = Symbol('y')
        self.first_equation = self.get_first_analytic_equation()
        self.second_equation = self.get_second_analytic_equation()
        self.first_callable_equation = self.get_first_callable_equation()
        self.second_callable_equation = self.get_second_callable_equation()

        self.precision = None
        self._dimension = dimension
        self._left_border = left_border
        self._right_border = right_border
        self._frequency = frequency

    def set_up_logger(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # ch = logging.StreamHandler()
        # ch.setLevel(logging.DEBUG)

        fh = logging.FileHandler(shared[LOG_FILE])
        fh.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # ch.setFormatter(formatter)
        fh.setFormatter(formatter)

        # self.logger.addHandler(ch)
        self.logger.addHandler(fh)

    def init_formulas(self):
        self.formulas = Formulas()
        Formulas.generator = self.generator
        Formulas.parameter = self.parameter

    def get_first_analytic_equation(self) -> Symbol:
        self.logger.debug(f"Start to get first analytical equation")

        def compute_equation(t1: Symbol, t2: Symbol) -> Symbol:
            return multiply(self.formulas.K_2(t1, t2), diff_list(self.formulas.K_2(t1, t2), t2, t2))

        if self.STORAGE_1.exists():
            self.logger.debug(f"An already calculated fist equation detected in {str(self.STORAGE_1)}. It's using")
            return restore_function(self.STORAGE_1)
        else:
            self.logger.debug(f"Start to calculate the first equation")
            equation = compute_equation(self.x, self.y)
            store_function(self.STORAGE_1, equation)
            self.logger.debug(f"The first equation calculated successfully")
            return equation

    def get_second_analytic_equation(self) -> Symbol:
        self.logger.debug(f"Start to get second analytical equation")

        def compute_equation(t1: Symbol, t2: Symbol) -> Symbol:
            term1 = 0.5 * (square(self.formulas.P(t1)) - square(self.formulas.K_1(t1, t2)))
            term2 = (0.5 * square(self.formulas.K_2(t1, t2)) + IonizationSymbols.I_p) * self.formulas.W(t1, t2)
            return term1 + term2

        if self.STORAGE_2.exists():
            self.logger.debug(f"An already calculated second equation detected in {str(self.STORAGE_1)}. It's using")
            return restore_function(self.STORAGE_2)
        else:
            self.logger.debug(f"Start to calculate the second equation")
            equation = compute_equation(self.x, self.y)
            store_function(self.STORAGE_2, equation)
            self.logger.debug(f"The second equation calculated successfully")
            return equation

    def get_first_callable_equation(self):
        callable_first = lambdify((self.x, self.y,
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
                                  self.first_equation,
                                  modules=[{"pi": numpy.pi}, {"Integral": real_quad}, 'sympy']
                                  )

        self.logger.info(f"The callable first equation {callable_first} created successfully")
        return callable_first

    def get_second_callable_equation(self):
        callable_second = lambdify((self.x, self.y,
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
                                   self.second_equation,
                                   modules=[{"pi": numpy.pi}, {"Integral": real_quad}, 'sympy']
                                   )

        self.logger.info(f"The callable second equation {callable_second} created successfully")
        return callable_second

    def solve(self) -> Iterable[SOLUTION]:
        self.logger.info(f"Start to find solution for parameter values: {str(self.parameter)}")

        def equation(arg):
            return [self.parametrized_first_equation(arg[0], arg[1]), self.parametrized_second_equation(arg[0], arg[1])]

        grid: ndarray = self.__get_grid()
        solutions: List[TwoValueSolution] = []

        for approx_point in grid:
            try:
                dirty_solution = excitingmixing(
                    equation,
                    approx_point
                )
                if dirty_solution is None:
                    raise ValueError(f"The NoneType solution returned")

                solution = TwoValueSolution(dirty_solution.item(0), dirty_solution.item(1))
                if solution not in solutions:
                    self.logger.info(
                        f"The solution: x = {solution.first_number}, y = {solution.second_number} is found")
                    solutions.append(solution)

            except (ValueError, ArithmeticError) as e:
                self.logger.error(f"The error: {str(e)} occurred")
            except NoConvergence:
                self.logger.error(f"A solution started from {approx_point} does not converge")

        return solutions

    def parametrized_first_equation(self, one1: Number, two1: Number) -> Number:
        return self.first_callable_equation(one1, two1,
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
                                            ).evalf()

    def parametrized_second_equation(self, one1: Number, two2: Number) -> Number:
        return self.second_callable_equation(one1, two2,
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
                                             ).evalf()

    def __get_grid(self) -> ndarray:
        basic_grid: ndarray = linspace(self._left_border, self._right_border, self._frequency)
        items = range(0, self._dimension)
        grid: ndarray = array([])

        for _ in items:
            grid = fill(grid, basic_grid)

        return grid

    def set_parameter(self, parameter: IonizationParameter):
        super().set_parameter(parameter)
        self.logger.info(f"The parameter {str(parameter)} is set")

    def set_precision(self, precision: float):
        TwoValueSolution.equal_round = precision
        self.logger.debug(f"The precision = {str(precision)} is set")
