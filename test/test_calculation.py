import unittest

from numpy import meshgrid, linspace
from numpy.ma import zeros, array, vstack, reshape
from scipy.optimize import fsolve

from src.consumer.Comsumer import Consumer
from src.util import fill
from test_equpment.envirnment.solution.TestSolution import TestSolution
from test_equpment.envirnment.solution.combiner.TestCombiner import TestCombiner
from test_equpment.envirnment.solver.TestSolver import TestSolver
from test_equpment.envirnment.stage.TestStage import TestStage


def problem(p):
    return p * p - 1


class CalculationTest(unittest.TestCase):
    def test_basic_calculation_works(self):
        """
        Try to solve equation
        | y1 = x1 ^ 2 - 1;
        | y2 = (x2 - 1) ^ 2 - 1.

        The solution should be approx: (1, 0), (-1, 0), (1, 2), (-1, 2)

        Registered stage just extracts the first value from every solution: 1, -1, 1, -1
        So finally solution should be its sum e.g. 0
        Note: generally it calculates complex values
        """
        combiner = TestCombiner()
        stages = [TestStage()]
        solver = TestSolver(problem, 2, -10, 10, 10)
        solver.set_precision(0.1)

        consumer = Consumer(combiner, stages)
        result = consumer.consume_by_solver(solver)
        self.assertEquals(result, 0 + 0j)

if __name__ == '__main__':
    unittest.main()
