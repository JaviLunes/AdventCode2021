# coding=utf-8
"""Tests for the Day 14: Extended Polymerization puzzle."""

# Standard library imports:
import unittest

# Local application imports:
from aoc2021.day_14.tools import Polymer


class ExampleTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        # noinspection SpellCheckingInspection
        self.recipe = [
            "NNCB", "", "CH -> B", "HH -> N", "CB -> H", "NH -> C", "HB -> C",
            "HC -> B", "HN -> C", "NN -> C", "BH -> H", "NC -> B", "NB -> B",
            "BN -> B", "BB -> N", "BC -> B", "CC -> N", "CN -> C"]

    def test_polymer_after_10_steps(self):
        """The polymer length is 3073, and the element frequency delta is 1588."""
        polymer = Polymer(recipe=self.recipe)
        polymer.polymerize_for(times=10)
        self.assertEqual(3073, polymer.length)
        self.assertEqual(1588, polymer.element_freq_delta)

    def test_polymer_after_40_steps(self):
        """The polymer element frequency delta is 2188189693529."""
        polymer = Polymer(recipe=self.recipe)
        polymer.polymerize_for(times=40)
        self.assertEqual(2188189693529, polymer.element_freq_delta)
