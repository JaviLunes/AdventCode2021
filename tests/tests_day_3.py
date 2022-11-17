# coding=utf-8
"""Tests for the Day 3: Binary Diagnostic puzzle."""

# Standard library imports:
import unittest

# Local application imports:
from aoc2021.day_3.tools import Report


class FirstExampleTests(unittest.TestCase):
    def setUp(self) -> None:
        """Prepare objects to be tested."""
        numbers = [
            "00100", "11110", "10110", "10111", "10101", "01111", "00111", "11100",
            "10000", "11001", "00010", "01010"]
        self.report = Report(*numbers)

    def test_gamma_rate(self):
        """The gamma rate must be 22."""
        self.assertEqual(22, self.report.gamma_rate)

    def test_epsilon_rate(self):
        """The epsilon rate must be 9."""
        self.assertEqual(9, self.report.epsilon_rate)

    def test_power_consumption(self):
        """The power consumption must be 198."""
        self.assertEqual(198, self.report.power_consumption)

    def test_o2_rating(self):
        """The O2 generator rating must be 23."""
        self.assertEqual(23, self.report.o2_rating)

    def test_co2_rating(self):
        """The C=2 scrubber rating must be 10."""
        self.assertEqual(10, self.report.co2_rating)

    def test_life_rating(self):
        """The life support rating must be 230."""
        self.assertEqual(230, self.report.life_rating)
