from src.solution.Solution import Solution
from src.stage.Stage import Stage
from test_equpment.envirnment.solution.TestSolution import TestSolution

StageWithComplexMember = Stage[TestSolution]


class TestStage(StageWithComplexMember):
    def get_result(self, test_solution: Solution) -> complex:
        return test_solution.get_solution()[0]
