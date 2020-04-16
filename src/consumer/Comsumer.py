from abc import abstractmethod
from typing import Generic, TypeVar, List, Callable

from src.solution.Solution import Solution
from src.solution.combiner.Combiner import Combiner
from src.solver.Solver import Solver
from src.stage.Stage import Stage

SolutionOrSub = TypeVar('SolutionOrSub', bound=Solution)
CombinerOrSub = TypeVar('CombinerOrSub', bound=Combiner)
AppropriateSolver = Solver[SolutionOrSub]


class Consumer(Generic[SolutionOrSub, CombinerOrSub]):
    def __init__(self, combiner: CombinerOrSub, stages: List[Stage[SolutionOrSub]]):
        self.combiner = combiner
        self.stages = stages

    def consume_by_solver(self, solver: AppropriateSolver) -> complex:
        solutions: List[Solution] = solver.solve()

        if len(solutions) == 0:
            raise Exception(f"There's no solutions provided by: {solver}")

        return sum([self.consume_solution(solution) for solution in solutions])

    def consume_solution(self, solution: Solution) -> complex:
        stage_results: List[complex] = [stage.get_result(solution) for stage in self.stages]
        reducer = lambda one, two: self.combiner.combine(one, two)
        return self.reduce(stage_results, reducer)

    @staticmethod
    def reduce(items: List[complex], reducer: Callable[[complex, complex], complex]) -> complex:
        if len(items) == 1:
            return items[0]

        result: complex = items[0]
        for number in range(1, len(items) - 1):
            result = reducer(result, items[number])
        return result
