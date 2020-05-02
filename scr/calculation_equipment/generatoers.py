from sympy import pi, exp, ln, Symbol

from scr.parameter.IonizationGeneratorParameter import IonizationGeneratorParameter
from scr.parameter.IonizationGeneratorSymbols import IonizationGeneratorSymbols
from scr.util import Number


def fading_generator(t: Symbol, parameter: IonizationGeneratorSymbols) -> Symbol:
    tay = 2 * pi * parameter.N / parameter.omega
    return exp((-2 * ln(2) * t ** 2) / (tay ** 2))
