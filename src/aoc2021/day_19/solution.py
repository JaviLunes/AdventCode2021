# coding=utf-8
"""Compute the solution of the Day 19: Beacon Scanner puzzle."""

# Third party imports:
import numpy

# Local application imports:
from aoc2021.common import read_puzzle_input
from aoc2021.day_19.tools import Constellation


def compute_solution() -> tuple[int, int]:
    """Compute the answers for the two parts of this day."""
    lines = read_puzzle_input(day=19)
    constellation = Constellation.from_report(report=lines)
    return len(constellation.beacons), numpy.max(constellation.scanner_distances)
