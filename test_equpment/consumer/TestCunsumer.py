# from scr.consumer.Consumer import Consumer, AppropriateSolver
# from scr.solution.combiner.AbstractCombiner import AbstractCombiner
# from test.enviornment.solution.TestSolution import TestSolution
# from test.enviornment.solution.combiner.TestCombiner import TestCombiner
# from test.enviornment.stage.TestStage import TestStage
#
#
# class TestConsumer(Consumer[TestSolution, TestCombiner]):
#     def __init__(self, test_combiner: AbstractCombiner):
#         super().__init__(test_combiner)
#
#         self._first_stage = TestStage()
#         self._second_stage = TestStage()
#
#     def consume_by_solver(self, solver: AppropriateSolver) -> complex:
#         final_result: complex = 0 + 0j
#
#         for solution in solver.solve():
#             first = self._first_stage.get_result(solution)
#             second = self._second_stage.get_result(solution)
#
#             final_result = final_result + super().combiner.combine(first, second)
#
#         return final_result
