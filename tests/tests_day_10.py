# coding=utf-8
"""Tests for the Day 10: Syntax Scoring puzzle."""

# Standard library imports:
import unittest

# Local application imports:
from aoc2021.day_10.tools import SyntaxChecker


class ExampleTests(unittest.TestCase):
    def setUp(self) -> None:
        """Prepare objects to be tested."""
        lines = [
            "[({(<(())[]>[[{[]{<()<>>",
            "[(()[<>])]({[<{<<[]>>(",
            "{([(<{}[<>[]}>{[]{[(<()>",
            "(((({<>}<{<{<>}{[]{[]{}",
            "[[<[([]))<([[{}[[()]]]",
            "[{[{({}]{}}([{[{{{}}([]",
            "{<[[]]>}<{[{[{[]{()[[[]",
            "[<(<(<(<{}))><([]([]()",
            "<{([([[(<>()){}]>(<<{{",
            "<{([{{}}[<[[[<>{}]]]>[]]"]
        self.checker = SyntaxChecker(lines=lines)

    def test_corruption_score(self):
        """The total score for corrupt lines is 26397."""
        self.assertEqual(26397, self.checker.corruption_score)

    def test_completion_score(self):
        """The total score for uncompleted lines is 288957."""
        self.assertEqual(288957, self.checker.completion_score)
