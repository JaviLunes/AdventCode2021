# coding=utf-8
"""Compute the solution of the Day 10: Syntax Scoring puzzle."""

# Local application imports:
from aoc2021.common import read_puzzle_input
from aoc2021.day_10.tools import SyntaxChecker


def compute_solution() -> tuple[int, int]:
    """Compute the answers for the two parts of this day."""
    lines = read_puzzle_input(day=10)
    checker = SyntaxChecker(lines=lines)
    return checker.corruption_score, checker.completion_score
