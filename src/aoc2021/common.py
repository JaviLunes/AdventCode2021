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


def build_all_templates():
    """Build templates for all non-existent day's puzzles."""
    for d in range(len(DAILY_NAMES)):
        build_templates(day=d + 1)


def build_templates(day: int):
    """Built input, tools, solving and tests template files for the provided day."""
    building_funcs = (_prepare_input, _prepare_solution, _prepare_tests, _prepare_tools)
    for func in building_funcs:
        file_path, lines = func(day=day)
        _write_file(file_path=file_path, lines=lines)


def _prepare_input(day: int):
    file_path = BASE_PATH / f"day_{day}" / "puzzle_input.txt"
    lines = [""]
    return file_path, lines


def _prepare_solution(day: int):
    file_path = BASE_PATH / f"day_{day}" / "solution.py"
    lines = [
        '# coding=utf-8\n',
        f'"""Compute the solution of the {DAILY_NAMES[day - 1]} puzzle."""\n',
        '\n',
        '# Local application imports:\n',
        'from aoc2021.common import read_puzzle_input\n',
        f'from aoc2021.day_{day}.tools import ...\n',
        '\n', '\n',
        'def compute_solution() -> tuple[int, int]:\n',
        '    """Compute the answers for the two parts of this day."""\n',
        f'    lines = read_puzzle_input(day={day})\n',
        '    ...\n',
        '    return None, None\n']
    return file_path, lines


def _prepare_tests(day: int):
    """Get file path and template lines for the testing file of the provided day."""
    file_path = BASE_PATH.parents[1] / "tests" / f"tests_day_{day}.py"
    lines = [
        '# coding=utf-8\n',
        f'"""Tests for the {DAILY_NAMES[day - 1]} puzzle."""\n',
        '\n',
        '# Standard library imports:\n',
        'import unittest\n',
        '\n',
        '# Local application imports:\n',
        f'from aoc2021.day_{day}.tools import ...\n',
        '\n', '\n',
        'class ExampleTests(unittest.TestCase):\n',
        '    def setUp(self) -> None:\n',
        '        """Define objects to be tested."""\n',
        '        ...\n']
    return file_path, lines


def _prepare_tools(day: int):
    file_path = BASE_PATH / f"day_{day}" / "tools.py"
    lines = [
        '# coding=utf-8\n',
        f'"""Tools used for solving the {DAILY_NAMES[day - 1]} puzzle."""\n',
        '\n']
    return file_path, lines


def _write_file(file_path: Path, lines: list[str]):
    """Create a new file and write lines, or silently fail if it already exists."""
    if file_path.exists():
        return
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file=file_path, mode="w") as file:
        file.writelines(lines)
