# coding=utf-8
"""Compute the solution of the Day 13: Transparent Origami puzzle."""

# Local application imports:
from aoc2021.common import read_puzzle_input
from aoc2021.day_13.tools import OrigamiInstructions


def compute_solution() -> tuple[int, str]:
    """Compute the answers for the two parts of this day."""
    lines = read_puzzle_input(day=13)
    origami = OrigamiInstructions(recipe=lines)
    origami.apply_folds(times=1)
    dots_after_one_fold = origami.visible_dots
    origami.apply_folds(times=None)
    return dots_after_one_fold, origami.sheet_code
