# coding=utf-8
"""Compute the solution of the Day 7: The Treachery of Whales puzzle."""

# Local application imports:
from aoc2021.common import read_puzzle_input
from aoc2021.day_7.tools import Crab, CrabSwarm


def compute_solution() -> tuple[int, int]:
    """Compute the answers for the two parts of this day."""
    lines = read_puzzle_input(day=7)
    start_positions = list(map(int, lines[0].split(",")))
    swarm = CrabSwarm(crabs=[Crab(position=p) for p in start_positions])
    _, lineal_cost = swarm.minimize_cost(linear=True)
    _, triangular_cost = swarm.minimize_cost(linear=False)
    return lineal_cost, triangular_cost
