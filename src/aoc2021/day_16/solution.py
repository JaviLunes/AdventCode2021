# coding=utf-8
"""Compute the solution of the Day 16: Packet Decoder puzzle."""

# Local application imports:
from aoc2021.common import read_puzzle_input
from aoc2021.day_16.tools import Packet


def compute_solution() -> tuple[int, int]:
    """Compute the answers for the two parts of this day."""
    lines = read_puzzle_input(day=16)
    packet = Packet.from_hexadecimal(hex_string="".join(lines))
    return packet.total_version, packet.value
