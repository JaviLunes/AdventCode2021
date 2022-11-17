# coding=utf-8
"""Tests for the Day 7: The Treachery of Whales puzzle."""

# Standard library imports:
import unittest

# Local application imports:
from aoc2021.day_7.tools import Crab, CrabSwarm


class ExampleTests(unittest.TestCase):
    def setUp(self) -> None:
        """Prepare objects to be tested."""
        start_positions = [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]
        self.swarm = CrabSwarm(crabs=[Crab(position=p) for p in start_positions])

    def test_optimum_linear_cost(self):
        """The best alignment position is 2, with a total cost of 37 fuel."""
        position, cost = self.swarm.minimize_cost(linear=True)
        self.assertEqual(2, position)
        self.assertEqual(37, cost)

    def test_optimum_triangular_cost(self):
        """The best alignment position is 5, with a total cost of 168 fuel."""
        position, cost = self.swarm.minimize_cost(linear=False)
        self.assertEqual(5, position)
        self.assertEqual(168, cost)
