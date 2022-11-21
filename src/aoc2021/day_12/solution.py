# coding=utf-8
"""Compute the solution of the Day 12: Passage Pathing puzzle."""

# Local application imports:
from aoc2021.common import read_puzzle_input
from aoc2021.day_12.tools import CaveSystem


def compute_solution() -> tuple[int, int]:
    """Compute the answers for the two parts of this day."""
    lines = read_puzzle_input(day=12)
    cave_system = CaveSystem.from_paths(paths=lines)
    paths_1 = cave_system.compute_valid_paths()
    paths_2 = cave_system.compute_relaxed_paths()
    return len(paths_1), len(paths_2)
