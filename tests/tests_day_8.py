# coding=utf-8
"""Tests for the Day 8: Seven Segment Search puzzle."""

# Standard library imports:
import unittest

# Local application imports:
from aoc2021.day_8.tools import Entry


class FirstExampleTests(unittest.TestCase):
    def setUp(self) -> None:
        """Prepare objects to be tested."""
        # noinspection SpellCheckingInspection
        texts = [
            "be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb |"
            "fdgacbe cefdb cefbgd gcbe",
            "edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec |"
            "fcgedb cgb dgebacf gc",
            "fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef |"
            "cg cg fdcagb cbg",
            "fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega |"
            "efabcd cedba gadfec cb",
            "aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga |"
            "gecf egdcabf bgf bfgea",
            "fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf |"
            "gebdcfa ecba ca fadegcb",
            "dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf |"
            "cefg dcbef fcge gbcadfe",
            "bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd |"
            "ed bcgafe cdgba cbgef",
            "egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg |"
            "gbdfcae bgc cg cgb",
            "gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc |"
            "fgae cfgab fg bagce"]
        self.entries = [Entry(entry_text=text) for text in texts]

    def test_count_digits_with_unique_segments_in_outputs(self):
        """The number of 1s, 4s, 7s and 8s instances in the outputs must be 26."""
        target_digits = ["1", "4", "7", "8"]
        total = 0
        for entry in self.entries:
            total += len([d for d in entry.output_digits if d in target_digits])
        self.assertEqual(26, total)

    def test_sum_output_values(self):
        """The sum of all four-digit output values must be 61229."""
        total = sum(int("".join(entry.output_digits)) for entry in self.entries)
        self.assertEqual(61229, total)
