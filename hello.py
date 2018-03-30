"""

Showcases a rather basic way to have multiple test data sets for a single unit test set.

Usage:

    # add 3 and 7 together, see if 10 comes out
    python test_addition.py
    # or
    TEST_DATA_CLASS=DevelopmentTestData python test_addition.py

    # add 1000 and 2000, make sure it's still 3000
    TEST_DATA_CLASS=ProductionTestData python test_addition.py

    # do 1+2, find out it's not 42
    TEST_DATA_CLASS=FailingTestData python test_addition.py

    # be reminded that you forgot to implement 'sum' in the test data class
    TEST_DATA_CLASS=IncompleteTestData python test_addition.py


"""

import os
import unittest
from abc import ABCMeta, abstractproperty

import sys


def add(x, y):
    """
    Adds two numbers; this is the method that's being tested.

    :param x: number 1
    :param y: number 2
    :returns: sum of two numbers
    """
    return x + y


class AbstractTestData:
    """Abstract test data class. Defines an interface for subclasses that contain test data."""

    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractproperty
    def operand_1(self):
        """Subclasses must have property 'operand_1' (first number to add)."""
        return NotImplemented

    @abstractproperty
    def operand_2(self):
        """Subclasses must have property 'operand_2' (second number to add)."""
        return NotImplemented

    @abstractproperty
    def sum(self):
        """Subclasses must have property 'sum' (expected sum of first and second numbers)."""
        return NotImplemented


class DevelopmentTestData(AbstractTestData):
    """Test data for testing against a "development" environment."""
    operand_1 = 3
    operand_2 = 7
    sum = 10


class ProductionTestData(AbstractTestData):
    """Test data for testing against a "production" environment."""
    operand_1 = 1000
    operand_2 = 2000
    sum = 3000


class FailingTestData(AbstractTestData):
    """Failing test data."""
    operand_1 = 1
    operand_2 = 2
    sum = 42


class IncompleteTestData(AbstractTestData):
    """Incomplete implementation of test data (no 'sum' property implemented)."""
    operand_1 = 32
    operand_2 = 64
    # sum = 1


class AbstractTestDataCase(unittest.TestCase):
    """
    Abstract unit test that test cases using the "dynamic" test data should derive from.

    Initializes instance of test data class into self.TEST_DATA that subclasses can later access.
    """

    ENV_KEY = 'TEST_DATA_CLASS'
    DEFAULT_TEST_DATA_CLASS_NAME = 'DevelopmentTestData'

    TEST_DATA = None

    def setUp(self):
        # Initialize instance of test data class
        test_data_class_name = os.getenv(AbstractTestDataCase.ENV_KEY,
                                         AbstractTestDataCase.DEFAULT_TEST_DATA_CLASS_NAME)
        test_data_class = getattr(sys.modules[__name__], test_data_class_name)
        self.TEST_DATA = test_data_class()


class AdditionTest(AbstractTestDataCase):
    """Unit test that tests add(x, y) defined above using the test data from the test data class."""

    def test(self):
        self.assertEqual(add(x=self.TEST_DATA.operand_1, y=self.TEST_DATA.operand_2), self.TEST_DATA.sum)


if __name__ == '__main__':
    unittest.main()
