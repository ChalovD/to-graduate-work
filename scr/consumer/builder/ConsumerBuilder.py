from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List

from scr.consumer.EuclidConsumer import Consumer
from scr.solution.AbstractSolution import AbstractSolution
from scr.solution.combiner import AbstractCombiner
from scr.stage import AbstractStage

Solution = TypeVar['Solution', AbstractSolution]


class SolverBuilder(ABC, Generic[Solution]):
    def __init__(self):
        self.stages: List[AbstractStage] = []
        self.combiner = None

    @abstractmethod
    def set_stage(self, stage: AbstractStage) -> None:
        self.stages.append(stage)

    @abstractmethod
    def set_combiner(self, combiner: AbstractCombiner) -> None:
        if self.combiner is not None:
            raise Exception(f"The combiner already assigned: {self.combiner}")
        self.combiner = combiner

    @abstractmethod
    def build_consumer(self) -> Consumer:
        return Consumer(self.combiner, self.stages)
