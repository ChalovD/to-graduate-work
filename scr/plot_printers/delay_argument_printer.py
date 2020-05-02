from mpmath import linspace

from scr import main
from scr.calculation_equipment.generatoers import fading_generator
from scr.consumer.EuclidConsumer import EuclidConsumer
from scr.main import LOG_FOLDER, LOG_FILE, shared
from scr.parameter.IonizationParameter import IonizationParameter
from scr.plot_printers.PlotPrinter import PlotPrinter
from scr.solver.EquationSolver import EquationSolver
from scr.stage.IonStage import IonStage
from scr.stage.PropelStage import PropelStage
from test_equpment.solution.combiner.MultiplyCombiner import MultiplyCombiner

X = 'T_d'
Y = 'A^2'

NAME = f"{Y}({X})"
shared[LOG_FILE] = LOG_FOLDER.joinpath(NAME)

FROM = 0
TO = 10
FREQUENCY = 15

X_VALUES = linspace(FROM, TO, FREQUENCY)

BASIC_PARAMETER = IonizationParameter()
BASIC_PARAMETER.T_d = 1
BASIC_PARAMETER.F = 1
BASIC_PARAMETER.omega_1 = 1
BASIC_PARAMETER.omega_2 = 2
BASIC_PARAMETER.etta_1 = -1
BASIC_PARAMETER.etta_2 = 1
BASIC_PARAMETER.N_1 = 1
BASIC_PARAMETER.N_2 = 2
BASIC_PARAMETER.f_0 = 2
BASIC_PARAMETER.I_p = 1
BASIC_PARAMETER.p = 1
BASIC_PARAMETER.p_theta = 1.5

COMBINER = MultiplyCombiner()

ION_STAGE = IonStage(fading_generator)
PROPEL_STAGE = PropelStage(fading_generator)
STAGES = [ION_STAGE, PROPEL_STAGE]

CONSUMER = EuclidConsumer(STAGES, COMBINER)

SOLVER = EquationSolver(fading_generator, 2, -10, 10, 4)
SOLVER.set_precision(0.001)


def calculator(arg: float) -> float:
    BASIC_PARAMETER.T_d = arg
    CONSUMER.set_parameter(BASIC_PARAMETER)

    result = CONSUMER.consume_by_solver(SOLVER)
    CONSUMER.clean()

    return result


if __name__ == "__main__":
    plot_printer = PlotPrinter(NAME, X_VALUES, calculator)
    plot_printer.set_x_label(X)
    plot_printer.set_y_label(Y)
    plot_printer.print()
