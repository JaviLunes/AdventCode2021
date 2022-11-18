# coding=utf-8
"""Compute the solution of the Day 1: Sonar Sweep puzzle."""

# Local application imports:
from aoc2021.common import read_puzzle_input
from aoc2021.day_1.tools import SonarReport


def compute_solution() -> tuple[int, int]:
    """Compute the answers for the two parts of this day."""
    lines = read_puzzle_input(day=1)
    report = SonarReport(measurements=list(map(int, lines)))
    return report.increments, report.sliding_increments
