# coding=utf-8
"""Compute the solution of the Day 9: Smoke Basin puzzle."""

# Local application imports:
from aoc2021.common import read_puzzle_input
from aoc2021.day_9.tools import Cave


def compute_solution() -> tuple[int, int]:
    """Compute the answers for the two parts of this day."""
    lines = read_puzzle_input(day=9)
    cave = Cave.from_row_strings(height_rows=lines)
    basin_caves = cave.explore_basins(impassable_height=9)
    sizes = sorted([c.size for c in basin_caves], reverse=True)
    return cave.total_risk_level, sizes[0] * sizes[1] * sizes[2]
