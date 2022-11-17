# coding=utf-8
"""Compute the solution of the Day 1: Sonar Sweep puzzle."""

# Local application imports:
from aoc2021.common import read_puzzle_input
from aoc2021.day_1.tools import SonarReport

print("\nDay 1: Sonar Sweep.")
lines = read_puzzle_input(day=1)
report = SonarReport(measurements=list(map(int, lines)))
# Part one:
print(f"    The solution to part one is: {report.increments}")

# Part two:
print(f"    The solution to part two is: {report.sliding_increments}")
