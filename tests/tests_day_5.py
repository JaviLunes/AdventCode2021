# coding=utf-8
"""Tests for the Day 5: Hydrothermal Venture puzzle."""

# Standard library imports:
import unittest

# Local application imports:
from aoc2021.day_5.tools import VentMap


class FirstExampleTests(unittest.TestCase):
    def setUp(self) -> None:
        """Prepare objects to be tested."""
        vents_lines = ["0, 9 -> 5, 9", "8, 0 -> 0, 8", "9, 4 -> 3, 4", "2, 2 -> 2, 1",
                       "7, 0 -> 7, 4", "6, 4 -> 2, 0", "0, 9 -> 2, 9", "3, 4 -> 1, 4",
                       "0, 0 -> 8, 8", "5, 5 -> 8, 2"]
        self.map_hv = VentMap(vent_segments=vents_lines, diagonals=False)
        self.map_hvd = VentMap(vent_segments=vents_lines, diagonals=True)

    def test_count_dangerous_points_hv(self):
        """The number of points with more than one vent line is 5."""
        self.assertEqual(5, len(self.map_hv.dangerous_points))

    def test_count_dangerous_points_hvd(self):
        """The number of points with more than one vent line is 12."""
        self.assertEqual(12, len(self.map_hvd.dangerous_points))
