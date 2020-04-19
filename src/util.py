from typing import Callable

from numpy.core.records import ndarray
from numpy.ma import empty, append, array
from sympy import symbols, diff, lambdify, integrate


def fill(destination: ndarray, source: ndarray):
    predictable_size: int

    if destination.size == 0:
        return array([array([member]) for member in source])
    else:
        predictable_size: int = destination.shape[1] + 1

    result: ndarray = empty((0, predictable_size), complex)

    for to_append in destination:
        for item in source:
            to_store = append(to_append, item)
            result = append(result, array([to_store]), axis=0)
    return result


class Integrate:
    VECTOR_DIMENSION: int

    @staticmethod
    def vector(function: Callable[[float], ndarray]) -> Callable[[float, float], ndarray]:
        arg = symbols('arg')
        down_bound = symbols('down_bound')
        up_bound = symbols('up_bound')

        items = range(0, Integrate.VECTOR_DIMENSION)
        results = [integrate(function(arg)[number], (arg, down_bound, up_bound)) for number in items]
        callable_results = [lambdify((down_bound, up_bound), result) for result in results]
        return lambda begin, end: array([callable_result(begin, end) for callable_result in callable_results])

    @staticmethod
    def scalar(function: Callable[[float], complex]) -> Callable[[float, float], complex]:
        arg = symbols('arg')
        down_bound = symbols('down_bound')
        up_bound = symbols('up_bound')

        result = integrate(function(arg), (arg, down_bound, up_bound))
        callable_results = lambdify((down_bound, up_bound), result)
        return callable_results


class Derivative:
    VECTOR_DIMENSION: int

    @staticmethod
    def one_argument_scalar_result(function: Callable[[complex], complex]) -> Callable[[complex], complex]:
        arg = symbols('arg')

        result = diff(function(arg), arg)
        callable_result = lambdify((arg,), result)

        return callable_result

    @staticmethod
    def two_arguments_scalar_result(function: Callable[[complex, complex], complex], order: int) -> Callable[
        [complex, complex], complex]:
        arg1 = symbols('arg1')
        arg2 = symbols('arg2')

        result = None
        if order == 1:
            result = diff(function(arg1, arg2), arg1)
        elif order == 2:
            result = diff(function(arg1, arg2), arg2)
        else:
            raise Exception(f"Only derivatives for 1st and 2nd order are supported. Got: {order}")

        callable_result = lambdify((arg1, arg2), result)
        return callable_result

    @staticmethod
    def one_argument_vector_result(function: Callable[[complex], ndarray]) -> Callable[[complex], ndarray]:
        arg = symbols('arg')

        items = range(0, Derivative.VECTOR_DIMENSION)
        results = [diff(function(arg), arg)[number] for number in items]
        callable_results = [lambdify((arg,), result) for result in results]
        return lambda argument: array([callable_result(argument) for callable_result in callable_results])

    @staticmethod
    def two_arguments_vector_result(function: Callable[[complex, complex], ndarray], order: int) -> Callable[
        [complex, complex], ndarray]:
        arg1 = symbols('arg1')
        arg2 = symbols('arg2')

        results = None
        items = range(0, Derivative.VECTOR_DIMENSION)
        if order == 1:
            results = [diff(function(arg1, arg2), arg1)[number] for number in items]
        elif order == 2:
            results = [diff(function(arg1, arg2), arg2)[number] for number in items]
        else:
            raise Exception(f"Only derivatives for 1st and 2nd order are supported. Got: {order}")

        callable_results = [lambdify((arg1, arg2), result) for result in results]
        return lambda argument1, argument2: array(
            [callable_result(argument1, argument2) for callable_result in callable_results])
