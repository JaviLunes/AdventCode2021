# coding=utf-8
"""Compute the solution of the Day 17: Trick Shot puzzle."""

# Local application imports:
from aoc2021.common import read_puzzle_input
from aoc2021.day_17.tools import ProbeLauncher


def compute_solution() -> tuple[int, int]:
    """Compute the answers for the two parts of this day."""
    lines = read_puzzle_input(day=17)
    launcher = ProbeLauncher.from_description(target_string="".join(lines))
    trick_shot_probe = launcher.launch_trick_shot(plot=False)
    valid_probes = launcher.find_valid_shots(plot=False)
    return trick_shot_probe.max_height, len(valid_probes)
