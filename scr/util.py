from pathlib import Path
from typing import Callable, Union, List

from numpy.core.records import ndarray
from numpy.ma import empty, append, array
from sympy import symbols, diff, lambdify, integrate, Symbol
from sympy.parsing.sympy_parser import parse_expr

Number = Union[float, complex]
Summable = Union[Number, Symbol]


def store_function(path: Path, function: Symbol) -> None:
    with path.open('w') as file:
        r = function.__str__()
        file.write(function.__str__())


def restore_function(path: Path) -> Symbol:
    with open(path, 'r') as file:
        return parse_expr(file.read())


# def sum_as_vectors(*terms: List[Summable]) -> List[Summable]:
    # result = None
    #
    # def add_current(current_term: List[Summable]) -> None:
    #     nonlocal result
    #     if result is None:
    #         result = current_term
    #     else:
    #         pairs = zip(result, current_term)
    #         result = [item_of_result + item_of_current_term for item_of_result, item_of_current_term in pairs]
    #
    # for term in terms:
    #     add_current(term)
    #
    # return result
def sum_as_vectors(term1: List[Summable], term2: List[Summable]) -> List[Summable]:
    vector = array(term1) + array(term2)
    return vector.tolist()


def multiply(first: List[Summable], second: List[Summable]) -> Summable:
    if not len(first) == len(second):
        raise Exception(f"Arguments have different sizes: {first}, {second} ")

    return sum([item_of_first * item_of_second for item_of_first, item_of_second in zip(first, second)])


def square(argument: List[Summable]) -> Summable:
    return multiply(argument, argument)


def increase(factor: Summable, vector: List[Summable]) -> List[Summable]:
    return [factor * vector_member for vector_member in vector]


def fill(destination: ndarray, source: ndarray):
    predictable_size: int

    if destination.size == 0:
        return array([array([member]) for member in source])
    else:
        predictable_size: int = destination.shape[1] + 1

    result: ndarray = empty((0, predictable_size), float)

    for to_append in destination:
        for item in source:
            to_store = append(to_append, item)
            result = append(result, array([to_store]), axis=0)
    return result


class Integrate:
    VECTOR_DIMENSION: int

    @staticmethod
    def vector(function: Callable[[Number], List[Number]]) -> Callable[[float, float], List[Number]]:
        arg = symbols('arg')
        down_bound = symbols('down_bound')
        up_bound = symbols('up_bound')

        items = range(0, Integrate.VECTOR_DIMENSION)
        results = [integrate(function(arg)[number], (arg, down_bound, up_bound)) for number in items]
        callable_results = [lambdify((down_bound, up_bound), result, 'sympy') for result in results]
        return lambda begin, end: [callable_result(begin, end) for callable_result in callable_results]

    @staticmethod
    def scalar(function: Callable[[Number], Number]) -> Callable[[Number, Number], Number]:
        arg = symbols('arg')
        down_bound = symbols('down_bound')
        up_bound = symbols('up_bound')

        result = integrate(function(arg), (arg, down_bound, up_bound))
        callable_results = lambdify((down_bound, up_bound), result, 'sympy')
        return callable_results


class Derivative:
    VECTOR_DIMENSION: int

    @staticmethod
    def one_argument_scalar_result(function: Callable[[Number], Number]) -> Callable[[Number], Number]:
        arg = symbols('arg')

        result = diff(function(arg), arg)
        callable_result = lambdify((arg,), result, 'sympy')

        return callable_result

    @staticmethod
    def two_arguments_scalar_result(function: Callable[[Number, Number], Number], order: int) \
            -> Callable[[Number, Number], Number]:
        arg1 = symbols('arg1')
        arg2 = symbols('arg2')

        if order == 1:
            result = diff(function(arg1, arg2), arg1)
        elif order == 2:
            result = diff(function(arg1, arg2), arg2)
        else:
            raise Exception(f"Only derivatives for 1st and 2nd order are supported. Got: {order}")

        callable_result = lambdify((arg1, arg2), result, 'sympy')
        return callable_result

    @staticmethod
    def one_argument_vector_result(function: Callable[[Number], List[Number]]) -> Callable[[Number], List[Number]]:
        arg = symbols('arg')

        items = range(0, Derivative.VECTOR_DIMENSION)
        results = [diff(function(arg)[number], arg) for number in items]
        callable_results = [lambdify((arg,), result, 'sympy') for result in results]
        return lambda argument: [callable_result(argument) for callable_result in callable_results]

    @staticmethod
    def two_arguments_vector_result(function: Callable[[Number, Number], List[Number]], order: int) \
            -> Callable[[Number, Number], List[Number]]:
        arg1 = symbols('arg1')
        arg2 = symbols('arg2')

        items = range(0, Derivative.VECTOR_DIMENSION)
        if order == 1:
            results = [diff(function(arg1, arg2)[number], arg1) for number in items]
        elif order == 2:
            results = [diff(function(arg1, arg2)[number], arg2) for number in items]
        else:
            raise Exception(f"Only derivatives for 1st and 2nd order are supported. Got: {order}")

        callable_results = [lambdify((arg1, arg2), result, 'sympy') for result in results]
        return lambda a1, a2: [callable_result(a1, a1) for callable_result in callable_results]
