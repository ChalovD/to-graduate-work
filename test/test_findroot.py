import unittest
from unittest import TestCase

from mpmath import findroot, matrix


def unsymmetrical_problem(x: float, y: float):
    return y - (x - 1) ** 2 - 1, x - 1, y - 1


class Test(TestCase):
    def test(self):
        actual_result = findroot(unsymmetrical_problem, (0, 0))
        expected_result = matrix([1., 1.])

        self.assertEqual(actual_result, expected_result)


if __name__ == '__main__':
    unittest.main()
