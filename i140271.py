
import os
import unittest
import sys


def add(x, y):
    """
    Adds two numbers; this is the method that's being tested.

    :param x: number 1
    :param y: number 2
    :returns: sum of two numbers
    """
    return x + y


def sub(x,y):

    return x-y

class AdditionTest(unittest.TestCase):
    """Unit test that tests add(x, y) defined above using the test data from the test data class."""

    def test1(self):
        self.assertEqual(add(5,5), 10)
    def test2(self):
        self.assertEqual(sub(5,5), 0)

if __name__ == '__main__':
    unittest.main()
