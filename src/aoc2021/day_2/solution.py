# coding=utf-8
"""Compute the solution of the Day 2: Dive! puzzle."""

# Local application imports:
from aoc2021.common import read_puzzle_input
from aoc2021.day_2.tools import Submarine, AimSubmarine

print("\nDay 2: Dive!")
lines = read_puzzle_input(day=2)
directions = [line.split()[0] for line in lines]
distances = [int(line.split()[1]) for line in lines]
course = list(zip(directions, distances))
submarine = Submarine()
submarine.implement_course(course=course)
# Part one:
print(f"    The solution to part one is: {submarine.total_movement}")

# Part two:
submarine = AimSubmarine()
submarine.implement_course(course=course)
print(f"    The solution to part two is: {submarine.total_movement}")
