import unittest
from unittest import TestCase
from numpy.ma import array
from scr.util import fill, sum_as_vectors, multiply, square, increase


class Test(TestCase):
    one = 1 + 3j
    two = 2 + 3j
    three = 3 + 3j
    four = 4 + 3j
    five = 5 + 3j

    def test_common_fill_works(self):
        destination = array([[self.one], [self.two]])
        source = array([self.three, self.four, self.five])
        actual_result = fill(destination, source)
        expected_result = array([[self.one, self.three], [self.one, self.four], [self.one, self.five],
                                 [self.two, self.three], [self.two, self.four], [self.two, self.five]])
        self.assertCountEqual(expected_result.tolist(), actual_result.tolist())

    def test_case_with_empty_destination_works(self):
        destination = array([])
        source = array([self.three, self.four, self.five])
        actual_result = fill(destination, source)
        expected_result = array([array([self.three]), array([self.four]), array([self.five])])
        self.assertCountEqual(expected_result.tolist(), actual_result.tolist())

    def test_sum_as_vectors(self):
        actual = sum_as_vectors([1, 2, 3], [4, 5, 6])
        expected = [5, 7, 9]

        self.assertEqual(actual, expected)

    def test_multiply(self):
        actual = multiply([1, 2, 3], [4, 5, 6])
        expected = 4. + 10. + 18.

        self.assertEqual(actual, expected)

    def test_square(self):
        actual = square([1, 2, 3])
        expected = 1. + 4. + 9.

        self.assertEqual(actual, expected)

    def test_increase(self):
        actual = increase(5., [1, 2, 3])
        expected = [5, 10, 15]

        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
