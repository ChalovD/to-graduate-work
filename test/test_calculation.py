import unittest

from mpmath import sqrt
from sympy import sin, exp, symbol, solveset, Symbol, symbols, nonlinsolve

from scr.consumer.EuclidConsumer import EuclidConsumer
from scr.parameter.IonizationParameter import IonizationParameter
from scr.util import Integrate
from test_equpment.parameter.ComplexNumberParameter import ComplexNumberParameter
from test_equpment.solution.combiner.MultiplyCombiner import MultiplyCombiner
from test_equpment.solver.EquationSolver import EquationSolver
from test_equpment.stage.ExtractFirstAndMultiplyByParameterStage import ExtractFirstAndMultiplyByParameterStage

DEFAULT_PARAMETER: complex = 0 + 0j


def parametrized_problem(x: complex, parameter: complex):
    return x * x - (parameter + (1 + 0j))


def problem(x: complex) -> complex:
    return parametrized_problem(x, DEFAULT_PARAMETER)


def problem_with_side_functions(x: complex, parameter: complex) -> complex:
    return sin(0.001 * exp(x)) + parameter


def problem_with_integral(x: complex, parameter: complex) -> complex:
    tu_integrate = lambda y: exp(-1. * y * y)

    integral = Integrate.scalar(tu_integrate)

    return integral(-100., x) - 1.1


class CalculationTest(unittest.TestCase):
    def test(self):
        combiner = MultiplyCombiner()

        stage = ExtractFirstAndMultiplyByParameterStage()
        stage.set_generator(parametrized_problem)
        stages = [stage]

        parameter = IonizationParameter()
        parameter.T_d = 1
        parameter.F = 1
        parameter.omega_1 = 1
        parameter.omega_2 = 2
        parameter.etta_1 = -1
        parameter.etta_2 = 1
        parameter.N_1 = 1
        parameter.N_2 = 2
        parameter.f_0 = 2
        parameter.I_p = 1
        parameter.p = 1
        parameter.p_theta = 1.5

        consumer = EuclidConsumer(stages, combiner)
        consumer.set_parameter(parameter)

        solver = EquationSolver(2, -10, 10, 3)
        solver.set_precision(0.1)
        solver.set_generator(problem_with_integral)

        result = consumer.consume_by_solver(solver)
        consumer.clean()
        self.assertEqual(result, 0)

    def test_basic_calculation_works(self):
        """
        Try to solve equation
        | y1 = x1 ^ 2 - 1;
        | y2 = (x2 - 1) ^ 2 - 1.

        The solution should be approx: (1, 0), (-1, 0), (1, 2), (-1, 2)

        Registered stage just extracts the first value (from every solution) multiplied by the parameter:
        1 * 0, -1 * 0, 1 * 0, -1 * 0
        So finally solution should be ( 0^2 + 0^2 + 0^2 + 0^2 )^(1/2) = 0
        Note: generally it calculates complex values
        """
        combiner = MultiplyCombiner()

        stage = ExtractFirstAndMultiplyByParameterStage()
        stage.set_generator(parametrized_problem)
        stages = [stage]

        parameter = ComplexNumberParameter()
        parameter.number = DEFAULT_PARAMETER

        consumer = EuclidConsumer(stages, combiner)
        consumer.set_parameter(parameter)

        solver = EquationSolver(2, -10, 10, 10)
        solver.set_precision(0.1)
        solver.set_generator(parametrized_problem)

        result = consumer.consume_by_solver(solver)
        consumer.clean()
        self.assertEqual(result, 0)

    def test_with_different_parameters(self):
        combiner = MultiplyCombiner()

        stage = ExtractFirstAndMultiplyByParameterStage()
        stage.set_generator(parametrized_problem)
        stages = [stage]

        solver = EquationSolver(2, -10, 10, 10)
        solver.set_precision(0.1)
        solver.set_generator(parametrized_problem)

        consumer = EuclidConsumer(stages, combiner)

        parameter1 = ComplexNumberParameter()
        parameter1.number = 3 + 0j
        consumer.set_parameter(parameter1)
        result1 = consumer.consume_by_solver(solver)
        consumer.clean()

        parameter2 = ComplexNumberParameter()
        parameter2.number = 8 + 0j
        consumer.set_parameter(parameter2)
        result2 = consumer.consume_by_solver(solver)
        consumer.clean()

        self.assertEqual(result1, sqrt(4 * (6 ** 2)))
        self.assertEqual(result2, sqrt(4 * (24 ** 2)))


if __name__ == '__main__':
    unittest.main()
