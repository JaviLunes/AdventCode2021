# coding=utf-8
"""Compute the solution of the Day 18: Snailfish puzzle."""

# Local application imports:
from aoc2021.common import read_puzzle_input
from aoc2021.day_18.tools import Homework


def compute_solution() -> tuple[int, int]:
    """Compute the answers for the two parts of this day."""
    lines = read_puzzle_input(day=18)
    homework = Homework(number_strings=lines)
    return homework.find_total_magnitude(), homework.find_max_twofold_magnitude()
