# coding=utf-8
"""Compute the solution of the Day 5: Hydrothermal Venture puzzle."""

# Local application imports:
from aoc2021.common import read_puzzle_input
from aoc2021.day_5.tools import VentMap


def compute_solution() -> tuple[int, int]:
    """Compute the answers for the two parts of this day."""
    lines = read_puzzle_input(day=5)
    vent_map_hv = VentMap(vent_segments=lines, diagonals=False)
    vent_map_hvd = VentMap(vent_segments=lines, diagonals=True)
    return len(vent_map_hv.dangerous_points), len(vent_map_hvd.dangerous_points)
