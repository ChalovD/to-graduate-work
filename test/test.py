import unittest
from math import pi

from numpy.core.records import ndarray
from numpy.ma import array
from sympy import sin, cos, exp

from src.util import Derivative, Integrate


class CalculationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        Derivative.VECTOR_DIMENSION = 2
        Integrate.VECTOR_DIMENSION = 3

    def test_one_argument_scalar_result_works(self):
        def f(x: complex) -> complex:
            return sin(x)

        derivative = Derivative.one_argument_scalar_result(f)

        self.assertEqual(1., derivative(0))

    def test_two_arguments_scalar_result_works(self):
        def f(x: complex, y: complex):
            return (x ** 2) * sin(y)

        derivative_by_x = Derivative.two_arguments_scalar_result(f, 1)
        derivative_by_y = Derivative.two_arguments_scalar_result(f, 2)

        self.assertEqual(2., derivative_by_x(1., pi / 2))
        self.assertEqual(1., derivative_by_y(1., 0.))

    def test_one_argument_vector_result_works(self):
        def f(t: complex):
            return array([
                cos(t),
                sin(t)
            ])

        derivative = Derivative.one_argument_vector_result(f)

        self.assertEquals([0., 1.], derivative(0).tolist())

    def test_two_arguments_vector_result_works(self):
        def f(x: complex, y: complex):
            return array([
                (x * y) ** 2,
                exp(2 * x * y)
            ])

        derivative_by_x = Derivative.two_arguments_vector_result(f, 1)
        derivative_by_y = Derivative.two_arguments_vector_result(f, 2)

        self.assertEqual([0, 0], derivative_by_x(0, 0).tolist())
        self.assertEqual([0, 0], derivative_by_y(0, 0).tolist())

    def test_scalar_integrate_works(self):
        def f(x: float) -> complex:
            return 2

        integral = Integrate.scalar(f)
        self.assertEqual(20, integral(0, 10))

    def test_vector_integrate_works(self):
        def f(x: float) -> ndarray:
            return array([
                1,
                2,
                3
            ])

        integral = Integrate.vector(f)
        self.assertEqual([10, 20, 30], integral(0, 10).tolist())
