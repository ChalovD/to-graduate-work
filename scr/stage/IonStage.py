import logging
from collections import Callable

import numpy
from sympy import exp, sqrt, pi, Symbol, lambdify

from scr.calculation_equipment.Formulas import Formulas, real_quad, complex_quad
from scr.main import FORMULAS, LOG_FILE, shared
from scr.parameter.IonizationGeneratorParameter import IonizationGeneratorParameter
from scr.parameter.IonizationParameter import IonizationParameter
from scr.parameter.IonizationSymbols import IonizationSymbols
from scr.solution.TwoValueSolution import TwoValueSolution
from scr.stage.AbstractStage import AbstractStage
from scr.util import Number, restore_function, store_function


class IonStage(AbstractStage[TwoValueSolution, IonizationParameter]):
    STORAGE = FORMULAS.joinpath('ion_stage')

    def __init__(self, generator):
        super().__init__(generator)
        self.logger = None
        self.set_up_logger()
        self.x = Symbol('x')
        self.y = Symbol('y')
        self.formulas = None
        self.init_formulas()
        self.stage = self.get_stage()
        self.callable_stage = self.get_callable_stage()

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

    def init_formulas(self):
        self.formulas = Formulas()
        Formulas.generator = self.generator
        Formulas.parameter = self.parameter

    def get_stage(self):
        self.logger.debug(f"Start to get {str(__name__)} analytical equation")

        def compute_stage(t1: Symbol, t2: Symbol) -> Symbol:
            numerator = IonizationSymbols.f_0 * exp(
                (- 1 * self.formulas.Kappa(t1, t2) ** 3) / (3 * self.formulas.F_tmp(t1, t2)))
            denominator = sqrt(4 * pi * self.formulas.Kappa(t1, t2) * self.formulas.F_tmp(t1, t2))

            return numerator / denominator

        if self.STORAGE.exists():
            self.logger.debug(f"An already calculated {__name__} equation detected in {str(self.STORAGE)}. It's using")
            return restore_function(self.STORAGE)
        else:
            self.logger.debug(f"Start to calculate the {__name__}")
            equation = compute_stage(self.x, self.y)
            store_function(self.STORAGE, equation)
            self.logger.debug(f"The {__name__} equation calculated successfully")
            return equation

    def get_callable_stage(self):
        callable_stage = lambdify((self.x, self.y,
                                   IonizationSymbols.T_d,
                                   IonizationSymbols.F,
                                   IonizationSymbols.omega_1,
                                   IonizationSymbols.omega_2,
                                   IonizationSymbols.etta_1,
                                   IonizationSymbols.etta_2,
                                   IonizationSymbols.N_1,
                                   IonizationSymbols.N_2,
                                   IonizationSymbols.f_0,
                                   IonizationSymbols.I_p,
                                   IonizationSymbols.p,
                                   IonizationSymbols.p_theta
                                   ),
                                  self.stage,
                                  modules=[{"pi": numpy.pi}, {"Integral": complex_quad}, 'sympy']
                                  )

        self.logger.info(f"The callable stage of {__name__} {callable_stage} created successfully")
        return callable_stage

    def get_result(self, solution: TwoValueSolution) -> Number:
        self.logger.debug(f"Start to calculate {__name__} for {str(solution)}")

        result = None
        try:
            result = self.parametrized_stage(solution.first_number, solution.second_number)
        except (ValueError, ArithmeticError) as e:
            self.logger.error(f"The error: {str(e)} occurred")

        self.logger.info(f"The {result} value calculated by {__name__}")
        return result

    def parametrized_stage(self, one1: Number, two1: Number) -> Number:
        return self.callable_stage(one1, two1,
                                   self.parameter.T_d,
                                   self.parameter.F,
                                   self.parameter.omega_1,
                                   self.parameter.omega_2,
                                   self.parameter.etta_1,
                                   self.parameter.etta_2,
                                   self.parameter.N_1,
                                   self.parameter.N_2,
                                   self.parameter.f_0,
                                   self.parameter.I_p,
                                   self.parameter.p,
                                   self.parameter.p_theta
                                   ).evalf()
