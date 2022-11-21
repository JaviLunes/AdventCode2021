# coding=utf-8
"""Compute the solution of the Day 11: Dumbo Octopus puzzle."""

# Local application imports:
from aoc2021.common import read_puzzle_input
from aoc2021.day_11.tools import OctopusGroup


def compute_solution() -> tuple[int, int]:
    """Compute the answers for the two parts of this day."""
    lines = read_puzzle_input(day=11)
    group_1 = OctopusGroup.from_strings(row_strings=lines)
    group_2 = OctopusGroup.from_strings(row_strings=lines)
    group_1.live_for(steps=100)
    return group_1.total_flashes, group_2.live_until_synchronicity()
