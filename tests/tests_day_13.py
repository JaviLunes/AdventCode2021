# coding=utf-8
"""Tests for the Day 13: Transparent Origami puzzle."""

# Standard library imports:
import unittest

# Local application imports:
from aoc2021.day_13.tools import OrigamiInstructions


class ExampleTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        self.instructions = [
            "6,10", "0,14", "9,10", "0,3", "10,4", "4,11", "6,0", "6,12", "4,1", "0,13",
            "10,12", "3,4", "3,0", "8,4", "1,10", "2,14", "8,10", "9,0", "",
            "fold along y=7", "fold along x=5"]

    def test_number_of_dots_after_one_fold(self):
        """The number of visible dots after applying one fold is 17."""
        origami = OrigamiInstructions(recipe=self.instructions)
        origami.apply_folds(times=1)
        self.assertEqual(17, origami.visible_dots)

    def test_number_of_dots_after_two_folds(self):
        """The number of visible dots after applying one fold is 16."""
        origami = OrigamiInstructions(recipe=self.instructions)
        origami.apply_folds(times=2)
        self.assertEqual(16, origami.visible_dots)
