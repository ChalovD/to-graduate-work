from src.solution.combiner.Combiner import Combiner


class TestCombiner(Combiner):
    def combine(self, first: complex, second: complex) -> complex:
        return first * second
