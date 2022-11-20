# coding=utf-8
"""Tests for the Day 9: Smoke Basin puzzle."""

# Standard library imports:
import unittest

# Local application imports:
from aoc2021.day_9.tools import Cave


class ExampleTests(unittest.TestCase):
    def setUp(self) -> None:
        """Prepare objects to be tested."""
        height_lines = [
            "2199943210", "3987894921", "9856789892", "8767896789", "9899965678"]
        self.cave = Cave.from_row_strings(height_rows=height_lines, wall_height=20)

    def test_count_local_low_points(self):
        """The number of local low points is 4."""
        self.assertEqual(4, self.cave.total_local_lows)

    def test_total_risk_level(self):
        """The total risk level for all low points is 15."""
        self.assertEqual(15, self.cave.total_risk_level)

    def test_number_of_basins(self):
        """The number of independent basins is 4."""
        self.assertEqual(4, len(self.cave.explore_basins(impassable_height=9)))

    def test_sizes_for_top_three_basins(self):
        """The top 3 larger basins have sizes of 14, 9 and 9."""
        basins = sorted(self.cave.explore_basins(impassable_height=9),
                        key=lambda c: c.size, reverse=True)
        sizes = [c.size for c in basins]
        self.assertListEqual([14, 9, 9], [c.size for c in basins[:3]])
        self.assertEqual(1134, sizes[0] * sizes[1] * sizes[2])
