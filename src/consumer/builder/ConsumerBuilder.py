from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from src.consumer.Comsumer import Consumer
from src.solution.Solution import Solution
from src.solution.combiner import Combiner
from src.stage import Stage

Solution = TypeVar['Solution', Solution]


class SolverBuilder(ABC, Generic[Solution]):
    @abstractmethod
    def set_stage(self, stage: Stage) -> None:
        pass

    @abstractmethod
    def set_combiner(self, combiner: Combiner) -> None:
        pass

    @abstractmethod
    def build_consumer(self) -> Consumer:
        pass
