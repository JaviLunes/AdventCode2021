# coding=utf-8
"""Tests for the Day 1: Sonar Sweep puzzle."""

# Standard library imports:
import unittest

# Local application imports:
from aoc2021.day_1.tools import SonarReport


class ExampleTests(unittest.TestCase):
    def setUp(self) -> None:
        """Prepare objects to be tested."""
        measurements = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]
        self.report = SonarReport(measurements=measurements)

    def test_direct_increments(self):
        """There are 7 increments in depth."""
        self.assertEqual(7, self.report.increments)

    def test_sliding_increments(self):
        """There are 5 3-measurement-sliding-window increments in depth."""
        self.assertEqual(5, self.report.sliding_increments)
