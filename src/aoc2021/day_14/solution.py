# coding=utf-8
"""Compute the solution of the Day 14: Extended Polymerization puzzle."""

# Local application imports:
from aoc2021.common import read_puzzle_input
from aoc2021.day_14.tools import Polymer


def compute_solution() -> tuple[int, int]:
    """Compute the answers for the two parts of this day."""
    lines = read_puzzle_input(day=14)
    polymer = Polymer(recipe=lines)
    polymer.polymerize_for(times=10)
    delta_after_10_steps = polymer.element_freq_delta
    polymer.polymerize_for(times=40 - 10)
    delta_after_40_steps = polymer.element_freq_delta
    return delta_after_10_steps, delta_after_40_steps
