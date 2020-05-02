import logging
from typing import Callable, List, Tuple

from quadpy import quad as quadpy_quad
from scipy.integrate import quad as scipy_quad
from sympy import sqrt, cos, sin, Symbol, lambdify, Integral, integrate, re, im

from scr.calculation_equipment.generatoers import fading_generator
from scr.main import LOG_FILE, shared
from scr.parameter.IonizationGeneratorSymbols import IonizationGeneratorSymbols
from scr.parameter.IonizationParameter import IonizationParameter
from scr.parameter.IonizationSymbols import IonizationSymbols
from scr.util import Number, sum_as_vectors, increase, square, multiply

logger = logging.getLogger(__name__)


def real_quad(expr, lims):
    var, a, b = lims
    a, b = polish_limits((a, b))
    return scipy_quad(lambdify(var, expr), a, b)[0]


def complex_quad(expr, lims):
    var, a, b = lims
    a, b = polish_limits((a, b))
    real = scipy_quad(lambdify(var, re(expr)), a, b)
    imagine = scipy_quad(lambdify(var, im(expr)), a, b)
    return complex(real[0], imagine[0])


def polish_limits(limits: Tuple[Number, Number]) -> Tuple[float, float]:
    a, b = limits
    if not (type(a) == complex or type(b) == complex):
        return limits
    if not type(a) == complex and type(b) == complex:
        if b.imag == 0:
            return a, b.real
        else:
            raise ValueError(f"Cannot integrate with essentially complex limits {limits}")
    if type(a) == complex and not type(b) == complex:
        if a.imag == 0:
            return a.real, b
        else:
            raise ValueError(f"Cannot integrate with essentially complex limits {limits}")
    if type(a) == complex and type(b) == complex:
        if a.imag == 0 and b.imag == 0:
            return a.real, b.real
        else:
            raise ValueError(f"Cannot integrate with essentially complex limits {limits}")


def diff_list(to_diff: List[Symbol], *args: Symbol) -> List[Symbol]:
    return [member.diff(*args) for member in to_diff]


def integrate_list(to_int: List[Symbol], tmp: Symbol, begin: Symbol, end: Symbol):
    return [member.integrate((tmp, begin, end)) for member in to_int]


def replace_one(items: List[Symbol], old: Symbol, new: Symbol) -> List[Symbol]:
    return [item.replace(old, new) for item in items]


def replace(items: List[Symbol], old: Tuple[Symbol, Symbol], new: Tuple[Symbol, Symbol]) -> List[Symbol]:
    return [item.replace(old[0], new[0]).replace(old[1], new[1]) for item in items]


class Formulas:
    generator: Callable[[Symbol, IonizationGeneratorSymbols], Number] = fading_generator

    R_1__value = None
    R_2__value = None
    R__value = None
    A__value = None
    F__value = None
    K_1__value = None
    K_2__value = None
    F_tmp__value = None
    F_tmp_square__value = None
    W__value = None
    P__value = None
    Kappa__value = None
    S__value = None
    L__value = None

    def __init__(self):
        self.logger = None
        self.set_up_logger()
        self.t = Symbol('t')
        self.t1 = Symbol('t1')
        self.t2 = Symbol('t2')

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

    def set_generator(self, generator: Callable[[Symbol, IonizationGeneratorSymbols], Symbol]):
        Formulas.generator = generator

    def set_parameter(self, parameter: IonizationParameter):
        Formulas.parameter = parameter
        self.set_generator_parameter()

    def set_generator_parameter(self):
        IonizationGeneratorSymbols.omega = IonizationSymbols.omega_1

    def omega_for_generator(self):
        return self.parameter.omega_1

    def get_impulse(self) -> List[Symbol]:
        return [
            IonizationSymbols.p * cos(IonizationSymbols.p_theta),
            IonizationSymbols.p * sin(IonizationSymbols.p_theta)
        ]

    def R_1(self, t: Symbol) -> List[Symbol]:
        if self.R_1__value is None:
            IonizationGeneratorSymbols.omega = IonizationSymbols.omega_1
            IonizationGeneratorSymbols.N = IonizationSymbols.N_1

            factor = (Formulas.generator(self.t, IonizationGeneratorSymbols) * IonizationSymbols.F) / (
                    IonizationSymbols.omega_1 ** 2)

            self.R_1__value = [
                factor * cos(IonizationSymbols.omega_1 * self.t),
                factor * IonizationSymbols.etta_1 * sin(IonizationSymbols.omega_1 * self.t)
            ]
            logger.info(f"The value for R_1 is set")
        return replace_one(self.R_1__value, self.t, t)

    def R_2(self, t: Symbol) -> List[Symbol]:
        if self.R_2__value is None:
            IonizationGeneratorSymbols.omega = IonizationSymbols.omega_1
            IonizationGeneratorSymbols.N = IonizationSymbols.N_2

            factor = (Formulas.generator(self.t, IonizationGeneratorSymbols) * IonizationSymbols.F) / (
                    IonizationSymbols.omega_2 ** 2)

            self.R_2__value = [
                factor * cos(IonizationSymbols.omega_2 * self.t),
                factor * IonizationSymbols.etta_1 * sin(IonizationSymbols.omega_2 * self.t)
            ]
            logger.info(f"The value for R_2 is set")

        return replace_one(self.R_2__value, self.t, t)

    def R(self, t: Symbol) -> List[Symbol]:
        if self.R__value is None:
            self.R__value = sum_as_vectors(
                self.R_1(self.t),
                self.R_2(self.t - IonizationSymbols.T_d)
            )
            logger.info(f"The value for R is set")

        return replace_one(self.R__value, self.t, t)

    def A(self, t: Symbol) -> List[Symbol]:
        if self.A__value is None:
            self.A__value = diff_list(self.R(self.t), self.t)
            logger.info(f"The value for A is set")

        return replace_one(self.A__value, self.t, t)

    def F(self, t: Symbol) -> List[Symbol]:
        if self.F__value is None:
            self.F__value = increase(-1., diff_list(self.A(self.t), self.t))
            logger.info(f"The value for F is set")

        return replace_one(self.F__value, self.t, t)

    def K_1(self, t1: Symbol, t2: Symbol) -> List[Symbol]:
        if self.K_1__value is None:
            integral = integrate_list(self.A(self.t), self.t, self.t2, self.t1)
            self.K_1__value = sum_as_vectors(
                self.A(self.t1),
                increase(-1 / (self.t1 - self.t2), integral)
            )
            logger.info(f"The value for K_1 is set")

        return replace(self.K_1__value, (self.t1, self.t2), (t1, t2))

    def K_2(self, t1: Symbol, t2: Symbol) -> List[Symbol]:
        if self.K_2__value is None:
            integral = integrate_list(self.A(self.t), self.t, self.t2, self.t1)
            self.K_2__value = sum_as_vectors(
                self.A(self.t1),
                increase(-1. / (self.t1 - self.t2), integral)
            )
            logger.info(f"The value for K_2 is set")

        return replace(self.K_2__value, (self.t1, self.t2), (t1, t2))

    def F_tmp_square(self, t1: Symbol, t2: Symbol) -> Symbol:
        if self.F_tmp_square__value is None:
            second_derivative = diff_list(self.K_2(self.t1, self.t2), self.t2, self.t2)
            self.F_tmp_square__value = square(second_derivative) + multiply(self.K_2(self.t1, self.t2),
                                                                            second_derivative)
            logger.info(f"The value for F_tmp_square is set")

        return self.F_tmp_square__value.replace(self.t1, t1).replace(self.t2, t2)

    def F_tmp(self, t1: Symbol, t2: Symbol) -> Symbol:
        if self.F_tmp__value is None:
            self.F_tmp__value = sqrt(self.F_tmp_square(t1, t2))
            logger.info(f"The value for F_tmp is set")

        return self.F_tmp__value.replace(self.t1, t1).replace(self.t2, t2)

    def W(self, t1: Symbol, t2: Symbol) -> Symbol:
        if self.W__value is None:
            first = 2. * multiply(self.K_1(self.t1, self.t2), self.K_2(self.t1, self.t2))
            second = multiply(self.F(self.t2),
                              sum_as_vectors(
                                  self.K_1(self.t1, self.t2),
                                  increase(-1., self.K_2(self.t1, self.t2))
                              )
                              )

            self.W__value = (first + second) / ((self.t1 - self.t2) * self.F_tmp_square(self.t1, self.t2))
            logger.info(f"The value for W is set")

        return self.W__value.replace(self.t1, t1).replace(self.t2, t2)

    def P(self, t: Symbol) -> List[Symbol]:
        if self.P__value is None:
            self.P__value = sum_as_vectors(
                self.get_impulse(),
                self.A(self.t)
            )
            logger.info(f"The value for P is set")

        return replace_one(self.P__value, self.t, t)

    def Kappa(self, t1: Symbol, t2: Symbol) -> Symbol:
        if self.Kappa__value is None:
            self.Kappa__value = sqrt(2. * IonizationSymbols.I_p + square(self.K_2(self.t1, self.t2)))
            logger.info(f"The value for Kappa is set")

        return self.Kappa__value.replace(self.t1, t1).replace(self.t2, t2)

    def S(self, t1: Symbol, t2: Symbol) -> Symbol:
        if self.S__value is None:
            # tmp1, tmp2 = symbols('tmp1, tmp2')

            inner_int = integrate_list(self.A(self.t), self.t, self.t2, self.t1)
            to_outer_integrating = square(sum_as_vectors(
                self.A(self.t),
                increase(-1. / (self.t1 - self.t2), inner_int)
            )
            )

            integral = Integral(to_outer_integrating, (self.t, self.t2, self.t1))  # TODO Stopgap measure

            self.S__value = -0.5 * integral + IonizationSymbols.I_p * self.t2 ** 2
            logger.info(f"The value for S is set")

        return self.S__value.replace(self.t1, t1).replace(self.t2, t2)

    def L(self, t1: Symbol, t2: Symbol) -> Symbol:
        if self.L__value is None:
            self.L__value = multiply(self.P(self.t1), diff_list(self.P(self.t1), self.t1)) - 1. * multiply(
                self.K_1(self.t1, self.t2),
                diff_list(self.K_1(self.t1, self.t2), self.t1)
            )
            logger.info(f"The value for L is set")

        return self.L__value.replace(self.t1, t1).replace(self.t2, t2)
