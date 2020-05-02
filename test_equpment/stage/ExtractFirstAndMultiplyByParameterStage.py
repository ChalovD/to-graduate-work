from scr.solution.AbstractSolution import AbstractSolution
from scr.stage.AbstractStage import AbstractStage
from test_equpment.parameter.ComplexNumberParameter import ComplexNumberParameter
from test_equpment.solution.ApproximateTwoDimensionComplexVectorSolution import \
    ApproximateTwoDimensionComplexVectorSolution

AppropriateStage = AbstractStage[ApproximateTwoDimensionComplexVectorSolution, ComplexNumberParameter]


class ExtractFirstAndMultiplyByParameterStage(AppropriateStage):
    def __init__(self):
        super().__init__()

    def get_result(self, test_solution: AbstractSolution) -> complex:
        return self.parameter.number * test_solution.get_solution()[0]
