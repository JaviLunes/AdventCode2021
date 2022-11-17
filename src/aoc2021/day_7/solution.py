# coding=utf-8
"""Compute the solution of the Day 7: The Treachery of Whales puzzle."""

# Local application imports:
from aoc2021.common import read_puzzle_input
from aoc2021.day_7.tools import Crab, CrabSwarm

print("\nDay 7: The Treachery of Whales.")
# Part one:
lines = read_puzzle_input(day=7)
start_positions = list(map(int, lines[0].split(",")))
swarm = CrabSwarm(crabs=[Crab(position=p) for p in start_positions])
_, optimum_cost = swarm.minimize_cost(linear=True)
print(f"    The solution to part one is: {optimum_cost}")

# Part two:
_, optimum_cost = swarm.minimize_cost(linear=False)
print(f"    The solution to part two is: {optimum_cost}")
