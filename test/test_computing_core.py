import unittest

from scr.calculation_equipment.generatoers import fading_generator
from scr.consumer.EuclidConsumer import EuclidConsumer
from scr.parameter.IonizationParameter import IonizationParameter
from scr.solution.TwoValueSolution import TwoValueSolution
from scr.solver.EquationSolver import EquationSolver
from scr.stage.IonStage import IonStage
from scr.stage.PropelStage import PropelStage
from test_equpment.solution.combiner.MultiplyCombiner import MultiplyCombiner


class CalculationTest(unittest.TestCase):
    def test_t(self):
        parameter = IonizationParameter()
        parameter.T_d = 1
        parameter.F = 1
        parameter.omega_1 = 1
        parameter.omega_2 = 2
        parameter.etta_1 = -1
        parameter.etta_2 = 1
        parameter.N_1 = 1
        parameter.N_2 = 2
        parameter.f_0 = 2
        parameter.I_p = 1
        parameter.p = 1
        parameter.p_theta = 1.5

        stage = PropelStage(fading_generator)
        stage.set_parameter(parameter)
        stage.get_result(TwoValueSolution(1, 2))

    def test(self):
        combiner = MultiplyCombiner()

        ion_stage = IonStage(fading_generator)
        propel_stage = PropelStage(fading_generator)
        stages = [ion_stage, propel_stage]

        parameter = IonizationParameter()
        parameter.T_d = 1
        parameter.F = 1
        parameter.omega_1 = 1
        parameter.omega_2 = 2
        parameter.etta_1 = -1
        parameter.etta_2 = 1
        parameter.N_1 = 1
        parameter.N_2 = 2
        parameter.f_0 = 2
        parameter.I_p = 1
        parameter.p = 1
        parameter.p_theta = 1.5

        consumer = EuclidConsumer(stages, combiner)
        consumer.set_parameter(parameter)

        solver = EquationSolver(fading_generator, 2, -10, 10, 10)
        solver.set_precision(0.1)
        result = consumer.consume_by_solver(solver)
        consumer.clean()
        print(result)
