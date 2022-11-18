# coding=utf-8
"""Shared tools used across different daily puzzles."""

# Standard library imports:
from importlib import import_module
from pathlib import Path

# Set constants:
BASE_PATH = Path(__file__).parent
# noinspection SpellCheckingInspection
DAILY_NAMES = tuple([
    "Day 1: Sonar Sweep", "Day 2: Dive", "Day 3: Binary Diagnostic",
    "Day 4: Giant Squid", "Day 5: Hydrothermal Venture", "Day 6: Lanternfish",
    "Day 7: The Treachery of Whales", "Day 8: Seven Segment Search",
    "Day 9: Smoke Basin", "Day 10: Syntax Scoring", "Day 11: Dumbo Octopus",
    "Day 12: Passage Pathing", "Day 13: Transparent Origami",
    "Day 14: Extended Polymerization", "Day 15: Chiton", "Day 16: Packet Decoder",
    "Day 17: Trick Shot", "Day 18: Snailfish", "Day 19: Beacon Scanner",
    "Day 20: Trench Map", "Day 21: Dirac Dice", "Day 22: Reactor Reboot",
    "Day 23: Amphipod", "Day 24: Arithmetic Logic Unit", "Day 25: Sea Cucumber"])


def compute_all_solutions():
    """Print the solutions for each of the available day's puzzles."""
    for d in range(len(DAILY_NAMES)):
        compute_solution(day=d + 1)


def compute_solution(day: int):
    """Print the two solutions for the target day's puzzle."""
    try:
        module = import_module(f"aoc2021.day_{day}.solution")
    except ModuleNotFoundError:
        return
    # noinspection PyBroadException
    try:
        print(f"\n{DAILY_NAMES[day - 1]}")
        solutions = module.compute_solution()
    except Exception:
        print("    The solution code for this puzzle failed!")
    else:
        print(f"    The solution to part one is: {solutions[0]}")
        print(f"    The solution to part two is: {solutions[1]}")


def read_puzzle_input(day: int) -> list[str]:
    """Read, process and return each line in the input file for the target day."""
    file_path = BASE_PATH / f"day_{day}" / "puzzle_input.txt"
    with open(file_path, mode="r") as file:
        lines = [line.removesuffix("\n") for line in file]
    return lines
