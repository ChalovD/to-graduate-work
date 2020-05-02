import logging
import os
import sys
import unittest
from pathlib import Path

from mpmath import findroot
from numpy import mgrid
from scipy.integrate import quad
from scipy.optimize import fsolve
from sympy import sin, symbols, nonlinsolve, lambdify, Symbol, exp, diff, symbol, integrate, cos

from scr.calculation_equipment.Formulas import Formulas
from scr.main import FORMULAS
from scr.util import Number, store_function, restore_function


def mach_solution_problem(x: Number, y: Number, parameter: Number):
    return [sin(parameter * x * y), 0]


def second(x: Number, y: Number, parameter: Number):
    return x + y + parameter


def integral_as_quad(expr, lims):
    var, a, b = lims
    return quad(lambdify(var, expr), a, b)[0]


class SolverTest(unittest.TestCase):
    x, y, p = symbols('x, y, p')

    def test_s(self):
       a = mgrid[0:5, 0:10]
       r = a.reshape((50, 2))
       f ='f'

    def test(self):
        x, y = symbols('x, y')
        x1, y1 = symbols('x1, x2')

        expr = cos(x * exp(y))
        expr1 = expr.replace(x, x1).replace(y, y1)

        r1 = first_sub(self.x, self.y)
        r2 = second_sub(self.x, self.y)
        r3 = third_sub(self.x, self.y)
        r4 = fourth_sub(self.x, self.y)

        logger = logging.getLogger(__name__)
        format = logging.Formatter('%(name)s : %(levelname)s : %(message)s')
        handler = logging.StreamHandler()
        handler.setFormatter(format)
        logger.addHandler(handler)
        logger.warning('This is a warning')

        f1 = lambdify((self.x, self.y), r1)
        f2 = lambdify((self.x, self.y), r2)
        f3 = lambdify((self.x, self.y), r3)
        f4 = lambdify((self.x, self.y), r4)

        v1 = f1(0, 2)
        v2 = f2(0, 2)
        v3 = f3(0, 2)
        v4 = f4(0, 2)

        equation = lambda z: f4(z, 2)

        res = fsolve(equation, 10)

    def test_storeability(self):
        original_function = fourth_sub(self.x, self.y)
        callable_from_original = lambdify((self.x, self.y), original_function)

        diff = original_function.diff(self.x)
        int = original_function.integrate(self.x, Symbol('t1'), Symbol('t2'))
        print(diff)
        print(int)
        file = FORMULAS.joinpath('test_storeability')
        store_function(file, original_function)
        restored_function = restore_function(file)
        callable_from_restored = lambdify((self.x, self.y), restored_function)

        self.assertEqual(callable_from_original(1, 1), callable_from_restored(1, 1))


def first_sub(x: Symbol, y: Symbol) -> Symbol:
    print('first_sub is called')
    return exp(x * y)


def second_sub(x: Symbol, y: Symbol) -> Symbol:
    print('second_sub is called')
    return diff(first_sub(x, y), x)


def third_sub(x: Symbol, y: Symbol) -> Symbol:
    print('third_sub is called')
    tmp = Symbol('tmp')
    return integrate(second_sub(x, tmp), (tmp, x, y))


def fourth_sub(x: Symbol, y: Symbol) -> Symbol:
    print('fourth_sub is called')
    return third_sub(x, y) ** 2
