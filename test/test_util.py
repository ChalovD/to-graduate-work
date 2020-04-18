import unittest
from unittest import TestCase
from numpy.ma import array
from src.util import fill


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


if __name__ == '__main__':
    unittest.main()
