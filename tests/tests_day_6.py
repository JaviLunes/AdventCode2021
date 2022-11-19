# coding=utf-8
"""Tests for the Day 6: Lanternfish puzzle."""

# Standard library imports:
import unittest

# Local application imports:
from aoc2021.day_6.tools import School


class ExampleTests(unittest.TestCase):
    def setUp(self) -> None:
        """Prepare objects to be tested."""
        self.initial_fishes = [3, 4, 3, 1, 2]

    def test_fishes_in_school_after_18_days(self):
        """The number of fishes in the school after 18 days is 26."""
        school = School(fish_states=self.initial_fishes)
        school.live_for(days=18)
        self.assertEqual(26, school.active_fishes)

    def test_fishes_in_school_after_80_days(self):
        """The number of fishes in the school after 80 days is 5934."""
        school = School(fish_states=self.initial_fishes)
        school.live_for(days=80)
        self.assertEqual(5934, school.active_fishes)

    def test_fishes_in_school_after_256_days(self):
        """The number of fishes in the school after 256 days is 26984457539."""
        school = School(fish_states=self.initial_fishes)
        school.live_for(days=256)
        self.assertEqual(26984457539, school.active_fishes)
