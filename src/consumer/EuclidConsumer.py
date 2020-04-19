from typing import List, Type, TypeVar

from mpmath import sqrt

from src.consumer.AbstractCnsumer import AbstractConsumer, SOLUTION, COMBINER, PARAMETER


class EuclidConsumer(AbstractConsumer[SOLUTION, COMBINER, PARAMETER]):
    def consume_result(self, results: List[complex]):
        return sqrt(sum([result ** 2 for result in results]))


# SolutionOrSub = TypeVar('SolutionOrSub', bound=AbstractSolution)
# CombinerOrSub = TypeVar('CombinerOrSub', bound=AbstractCombiner)
# AppropriateSolver = AbstractSolver[SolutionOrSub, Parameter]
#
#
# class Consumer(Generic[SolutionOrSub, CombinerOrSub]):
#     def __init__(self, combiner: CombinerOrSub, stages: List[AbstractStage[SolutionOrSub]]):
#         self.combiner = combiner
#         self.stages = stages
#
#     def consume_by_solver(self, solver: AppropriateSolver) -> complex:
#         solutions: List[AbstractSolution] = solver.solve()
#
#         if len(solutions) == 0:
#             raise Exception(f"There's no solutions provided by: {solver}")
#
#         return sqrt(sum([self.consume_solution(solution) ** 2 for solution in solutions]))
#
#     def consume_solution(self, solution: AbstractSolution) -> complex:
#         stage_results: List[complex] = [stage.get_result(solution) for stage in self.stages]
#         reducer = lambda one, two: self.combiner.combine(one, two)
#         return self.reduce(stage_results, reducer)
#
#     @staticmethod
#     def reduce(items: List[complex], reducer: Callable[[complex, complex], complex]) -> complex:
#         if len(items) == 1:
#             return items[0]
#
#         result: complex = items[0]
#         for number in range(1, len(items) - 1):
#             result = reducer(result, items[number])
#         return result
