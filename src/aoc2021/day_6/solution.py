# coding=utf-8
"""Compute the solution of the Day 6: Lanternfish puzzle."""

# Local application imports:
from aoc2021.common import read_puzzle_input
from aoc2021.day_6.tools import School


def compute_solution() -> tuple[int, int]:
    """Compute the answers for the two parts of this day."""
    lines = read_puzzle_input(day=6)
    school_1 = School(fish_states=list(map(int, lines[0].split(","))))
    school_2 = School(fish_states=list(map(int, lines[0].split(","))))
    school_1.live_for(days=80)
    school_2.live_for(days=256)
    return school_1.active_fishes, school_2.active_fishes
