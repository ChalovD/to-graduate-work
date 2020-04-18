import unittest

from src.consumer.Comsumer import Consumer
from test_equpment.envirnment.solution.combiner.TestCombiner import TestCombiner
from test_equpment.envirnment.solver.TestSolver import TestSolver
from test_equpment.envirnment.stage.TestStage import TestStage

DEFAULT_PARAMETER: complex = 0 + 0j


def parametrized_problem(x: complex, parameter: complex):
    return x * x - (parameter + (1 + 0j))


def problem(x: complex) -> complex:
    return parametrized_problem(x, DEFAULT_PARAMETER)


class CalculationTest(unittest.TestCase):
    def test_basic_calculation_works(self):
        """
        Try to solve equation
        | y1 = x1 ^ 2 - 1;
        | y2 = (x2 - 1) ^ 2 - 1.

        The solution should be approx: (1, 0), (-1, 0), (1, 2), (-1, 2)

        Registered stage just extracts the first value from every solution: 1, -1, 1, -1
        So finally solution should be ( 1^2 + (-1)^2 + 1^2 + (-1)^2 )^(1/2) = 2
        Note: generally it calculates complex values
        """
        combiner = TestCombiner()
        stages = [TestStage()]
        solver = TestSolver(parametrized_problem, 2, -10, 10, 10)
        solver.set_precision(0.1)
        consumer = Consumer(combiner, stages)

        solver.set_parameter(DEFAULT_PARAMETER)
        result = consumer.consume_by_solver(solver)
        self.assertEquals(2 + 0j, result)

    def test(self):
        combiner = TestCombiner()
        stages = [TestStage()]
        solver = TestSolver(parametrized_problem, 2, -10, 10, 10)
        solver.set_precision(0.1)
        consumer = Consumer(combiner, stages)

        solver.set_parameter(3 + 0j)
        result1 = consumer.consume_by_solver(solver)
        solver.set_parameter(8 + 0j)
        result2 = consumer.consume_by_solver(solver)

        self.assertEqual(4 + 0j, result1)
        self.assertEquals(6 + 0j, result2)


if __name__ == '__main__':
    unittest.main()
