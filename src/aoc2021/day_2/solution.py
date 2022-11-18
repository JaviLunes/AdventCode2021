# coding=utf-8
"""Compute the solution of the Day 2: Dive! puzzle."""

# Local application imports:
from aoc2021.common import read_puzzle_input
from aoc2021.day_2.tools import Submarine, AimSubmarine


def compute_solution() -> tuple[int, int]:
    """Compute the answers for the two parts of this day."""
    lines = read_puzzle_input(day=2)
    directions = [line.split()[0] for line in lines]
    distances = [int(line.split()[1]) for line in lines]
    course = list(zip(directions, distances))
    submarine = Submarine()
    submarine.implement_course(course=course)
    aim_submarine = AimSubmarine()
    aim_submarine.implement_course(course=course)
    return submarine.total_movement, aim_submarine.total_movement
