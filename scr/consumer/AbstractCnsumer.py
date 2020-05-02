import logging
from abc import ABC, abstractmethod
from typing import Generic, List, Callable, TypeVar

from scr.main import shared, LOG_FILE
from scr.parameter.AbstaractParameter import AbstractParameter
from scr.solution.AbstractSolution import AbstractSolution
from scr.solution.combiner.AbstractCombiner import AbstractCombiner
from scr.solver.AbstractSolver import AbstractSolver
from scr.stage.AbstractStage import AbstractStage

SOLUTION = TypeVar('SOLUTION', bound=AbstractSolution)
COMBINER = TypeVar('COMBINER', bound=AbstractCombiner)
PARAMETER = TypeVar('PARAMETER', bound=AbstractParameter)


class AbstractConsumer(ABC, Generic[SOLUTION, COMBINER, PARAMETER]):
    def __init__(self, stages: List[AbstractStage[PARAMETER, SOLUTION]], combiner: COMBINER) -> None:
        self.logger = None
        self.set_up_logger()
        self.stages = stages
        self.combiner = combiner
        self.parameter = None  # Should be set in the appropriate setter
        self.processed_solutions: List[complex] = []

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

    def set_parameter(self, parameter: PARAMETER):
        self.parameter = parameter
        for stage in self.stages:
            stage.set_parameter(parameter)

    def consume_by_solver(self, solver: AbstractSolver[SOLUTION, PARAMETER]) -> float:
        solver.set_parameter(self.parameter)

        solutions: List[SOLUTION] = solver.solve()
        try:
            self.validate_solutions(solver, solutions)
        except Exception:
            self.logger.error(f"There's no solutions. It's assumed that hre result should be 0")
            return 0

        for solution in solutions:
            self.process_solution(solution)

        return self.consume_result(self.processed_solutions)

    def clean(self):
        self.parameter = None
        self.processed_solutions = []

    @staticmethod
    def validate_solutions(solver: AbstractSolver[SOLUTION, PARAMETER], solutions: List[SOLUTION]):
        if len(solutions) == 0:
            raise Exception(f"There's no solutions provided by: {solver}")

    def process_solution(self, solution: SOLUTION):
        stage_calculations: List[complex] = [stage.get_result(solution) for stage in self.stages]
        result = self.reduce(stage_calculations, self.combiner.combine)
        self.processed_solutions.append(result)

    @staticmethod
    def reduce(items: List[complex], reducer: Callable[[complex, complex], complex]) -> complex:
        if len(items) == 1:
            return items[0]

        result: complex = items[0]
        for number in range(1, len(items) - 1):
            result = reducer(result, items[number])
        return result

    @abstractmethod
    def consume_result(self, results: List[complex]):
        pass
