# coding=utf-8
"""Compute the solution of the Day 8: Seven Segment Search puzzle."""

# Local application imports:
from aoc2021.common import read_puzzle_input
from aoc2021.day_8.tools import Entry


def compute_solution() -> tuple[int, int]:
    """Compute the answers for the two parts of this day."""
    targets = ["1", "4", "7", "8"]
    texts = read_puzzle_input(day=8)
    entries = [Entry(entry_text=text) for text in texts]
    total_1 = sum(len([d for d in e.output_digits if d in targets]) for e in entries)
    total_2 = sum(int("".join(entry.output_digits)) for entry in entries)
    return total_1, total_2
