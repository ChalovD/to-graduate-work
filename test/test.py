import unittest
from math import pi
from typing import List

from sympy import sin, cos, exp

from scr.util import Derivative, Integrate, Number


class CalculationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        Derivative.VECTOR_DIMENSION = 2
        Integrate.VECTOR_DIMENSION = 3

    def test_one_argument_scalar_result_works(self):
        def f(x: Number) -> Number:
            return sin(x)

        derivative = Derivative.one_argument_scalar_result(f)

        self.assertEqual(1., derivative(0))

    def test_two_arguments_scalar_result_works(self):
        def f(x: Number, y: Number) -> Number:
            return (x ** 2) * sin(y)

        derivative_by_x = Derivative.two_arguments_scalar_result(f, 1)
        derivative_by_y = Derivative.two_arguments_scalar_result(f, 2)

        self.assertEqual(2., derivative_by_x(1., pi / 2))
        self.assertEqual(1., derivative_by_y(1., 0.))

    def test_one_argument_vector_result_works(self):
        def f(t: Number) -> List[Number]:
            return [
                cos(t),
                sin(t)
            ]

        derivative = Derivative.one_argument_vector_result(f)

        self.assertEquals([0., 1.], derivative(0))

    def test_two_arguments_vector_result_works(self):
        def f(x: Number, y: Number) -> List[Number]:
            return [
                (x * y) ** 2,
                exp(2 * x * y)
            ]

        derivative_by_x = Derivative.two_arguments_vector_result(f, 1)
        derivative_by_y = Derivative.two_arguments_vector_result(f, 2)

        self.assertEqual([0, 0], derivative_by_x(0, 0))
        self.assertEqual([0, 0], derivative_by_y(0, 0))

    def test_scalar_integrate_works(self):
        def f(x: Number) -> Number:
            return 2

        integral = Integrate.scalar(f)
        self.assertEqual(20, integral(0, 10))

    def test_vector_integrate_works(self):
        def f(x: Number) -> List[Number]:
            return [
                1,
                2,
                3
            ]

        integral = Integrate.vector(f)
        self.assertEqual([10, 20, 30], integral(0, 10))

    def test(self):
        instance = ForDerivative(1 + 1j)

        res = instance.wrapped(1 + 1j)


class ForDerivative:
    def __init__(self, parameter: Number):
        self.parameter = parameter

    def wrapped(self, x: Number):
        res = Derivative.one_argument_vector_result(self.derivative_me)
        return res(x)

    def derivative_me(self, x: Number) -> List[Number]:
        return [
            cos(self.parameter * self.x_func(x)),
            sin(self.parameter * self.y_func(2 * x))
        ]

    def x_func(self, x: Number):
        return exp(self.parameter * x)

    def y_func(self, y: Number):
        return exp(self.parameter * y)
