from src.solution.combiner.AbstractCombiner import AbstractCombiner


class MultiplyCombiner(AbstractCombiner):
    def combine(self, first: complex, second: complex) -> complex:
        return first * second
