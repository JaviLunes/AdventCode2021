# coding=utf-8
"""Tests for the Day 11: Dumbo Octopus puzzle."""

# Standard library imports:
import unittest

# Local application imports:
from aoc2021.day_11.tools import OctopusGroup


class ExampleTests(unittest.TestCase):
    def setUp(self) -> None:
        """Prepare objects to be tested."""
        self.energy_rows = [
            "5483143223", "2745854711", "5264556173", "6141336146", "6357385478",
            "4167524645", "2176841721", "6882881134", "4846848554", "5283751526"]

    def test_flashes_after_10_steps(self):
        """After 10 steps, the total number of flashes is 204."""
        group = OctopusGroup.from_strings(row_strings=self.energy_rows)
        group.live_for(steps=10)
        self.assertEqual(204, group.total_flashes)

    def test_flashes_after_100_steps(self):
        """After 100 steps, the total number of flashes is 1656."""
        group = OctopusGroup.from_strings(row_strings=self.energy_rows)
        group.live_for(steps=100)
        self.assertEqual(1656, group.total_flashes)

    def test_flash_until_synchronicity(self):
        """The first fully synchronous flash is achieved at step 195."""
        group = OctopusGroup.from_strings(row_strings=self.energy_rows)
        self.assertEqual(195, group.live_until_synchronicity())
