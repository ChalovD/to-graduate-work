from typing import List

from scr.solution.AbstractSolution import AbstractSolution


class TwoValueSolution(AbstractSolution[List[complex]]):
    equal_round = None

    @classmethod
    def set_equal_round(cls, equal_round: float):
        cls.equal_round = equal_round

    @classmethod
    def get_equal_round(cls):
        return cls.equal_round

    def __init__(self, first_number: complex, second_number: complex):
        super().__init__()

        self.first_number = first_number
        self.second_number = second_number

    def __eq__(self, other):
        return abs(self.__calculate_metric(other)) < self.equal_round

    def __hash__(self):
        return 42

    def __calculate_metric(self, other):
        return ((self.first_number - other.first_number) ** 2) + ((self.second_number - other.second_number) ** 2)

    def get_solution(self) -> List[complex]:
        return [self.first_number, self.second_number]
