# coding=utf-8
"""Compute the solution of the Day 15: Chiton puzzle."""

# Local application imports:
from aoc2021.common import read_puzzle_input
from aoc2021.day_15.tools import ChironCave, ExpandedChironCave


def compute_solution() -> tuple[int, int]:
    """Compute the answers for the two parts of this day."""
    lines = read_puzzle_input(day=15)
    cave_small = ChironCave(risk_levels=lines)
    cave_large = ExpandedChironCave(risk_levels=lines)
    best_risk_small = cave_small.get_minimum_total_risk(include_start=False)
    best_risk_large = cave_large.get_minimum_total_risk(include_start=False)
    return best_risk_small, best_risk_large
