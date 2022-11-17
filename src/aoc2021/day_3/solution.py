# coding=utf-8
"""Compute the solution of the Day 3: Binary Diagnostic puzzle."""

# Local application imports:
from aoc2021.common import read_puzzle_input
from aoc2021.day_3.tools import Report

print("\nDay 3: Binary Diagnostic.")
# Part one:
numbers = read_puzzle_input(day=3)
report = Report(*numbers)
print(f"    The solution to part one is: {report.power_consumption}")

# Part two:
print(f"    The solution to part two is: {report.life_rating}")
