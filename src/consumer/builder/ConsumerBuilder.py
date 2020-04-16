from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List

from src.consumer.Comsumer import Consumer
from src.solution.Solution import Solution
from src.solution.combiner import Combiner
from src.stage import Stage

Solution = TypeVar['Solution', Solution]


class SolverBuilder(ABC, Generic[Solution]):
    def __init__(self):
        self.stages: List[Stage] = []
        self.combiner = None

    @abstractmethod
    def set_stage(self, stage: Stage) -> None:
        self.stages.append(stage)

    @abstractmethod
    def set_combiner(self, combiner: Combiner) -> None:
        if self.combiner is not None:
            raise Exception(f"The combiner already assigned: {self.combiner}")
        self.combiner = combiner

    @abstractmethod
    def build_consumer(self) -> Consumer:
        return Consumer(self.combiner, self.stages)
