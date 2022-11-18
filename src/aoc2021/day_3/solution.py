# coding=utf-8
"""Compute the solution of the Day 3: Binary Diagnostic puzzle."""

# Local application imports:
from aoc2021.common import read_puzzle_input
from aoc2021.day_3.tools import Report


def compute_solution() -> tuple[int, int]:
    """Compute the answers for the two parts of this day."""
    numbers = read_puzzle_input(day=3)
    report = Report(*numbers)
    return report.power_consumption, report.life_rating
