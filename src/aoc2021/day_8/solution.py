# coding=utf-8
"""Compute the solution of the Day 8: Seven Segment Search puzzle."""

# Local application imports:
from aoc2021.common import read_puzzle_input
from aoc2021.day_8.tools import Entry

print("\nDay 8: Seven Segment Search.")
# Part one:
targets = ["1", "4", "7", "8"]
texts = read_puzzle_input(day=8)
entries = [Entry(entry_text=text) for text in texts]
total = sum(len([d for d in entry.output_digits if d in targets]) for entry in entries)
print(f"    The solution to part one is: {total}")

# Part two:
total = sum(int("".join(entry.output_digits)) for entry in entries)
print(f"    The solution to part two is: {total}")
