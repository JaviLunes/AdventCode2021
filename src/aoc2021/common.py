# coding=utf-8
"""Shared tools used across different daily puzzles."""

# Standard library imports:
from importlib import import_module
from pathlib import Path
from time import time

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


def read_puzzle_input(day: int) -> list[str]:
    """Read, process and return each line in the input file for the target day."""
    file_path = BASE_PATH / f"day_{day}" / "puzzle_input.txt"
    with open(file_path, mode="r") as file:
        lines = [line.removesuffix("\n") for line in file]
    return lines


class AdventBuilder:
    """Manage template file building tasks."""
    def build_templates(self, day: int):
        """Built input, tools, solving and tests template files for the provided day."""
        self._write_file(*self._prepare_input(day=day))
        self._write_file(*self._prepare_solution(day=day))
        self._write_file(*self._prepare_tests(day=day))
        self._write_file(*self._prepare_tools(day=day))

    def build_all_templates(self):
        """Built input, tools, solving and tests template files for all days."""
        for day in range(1, len(DAILY_NAMES) + 1):
            self.build_templates(day=day)

    @staticmethod
    def _write_file(file_path: Path, lines: list[str]):
        """Create a new file and write lines, or silently fail if it already exists."""
        if not file_path.exists():
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file=file_path, mode="w") as file:
                file.writelines(lines)

    @staticmethod
    def _prepare_input(day: int) -> tuple[Path, list[str]]:
        """Get file path and content lines for the puzzle input file."""
        return BASE_PATH / f"day_{day}" / "puzzle_input.txt", [""]

    @staticmethod
    def _prepare_solution(day: int) -> tuple[Path, list[str]]:
        """Get file path and content lines for the puzzle-solving script file."""
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

    @staticmethod
    def _prepare_tests(day: int) -> tuple[Path, list[str]]:
        """Get file path and content lines for the tool-testing script file."""
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

    @staticmethod
    def _prepare_tools(day: int):
        """Get file path and content lines for the tool module file."""
        file_path = BASE_PATH / f"day_{day}" / "tools.py"
        lines = [
            '# coding=utf-8\n',
            f'"""Tools used for solving the {DAILY_NAMES[day - 1]} puzzle."""\n',
            '\n']
        return file_path, lines


class AdventSolver:
    """Manage puzzle solving tasks."""
    def print_day(self, day: int):
        """Print the solutions and execution time for the target day's puzzles."""
        print(DAILY_NAMES[day - 1])
        solution_1, solution_2, timing = self.solve_day(day=day)
        if solution_1 is None:
            print("    The first puzzle remains unsolved!")
        else:
            print(f"    The first solution is {solution_1}.")
        if solution_2 is None:
            print("    The second puzzle remains unsolved!")
        else:
            print(f"    The second solution is {solution_2}.")
        if solution_1 is not None or solution_2 is not None:
            print(f"    This took {timing}.")

    def print_all_days(self):
        """Print the solutions and execution times for each day's puzzles."""
        for day in range(1, len(DAILY_NAMES) + 1):
            self.print_day(day=day)

    def solve_day(self, day: int) -> tuple[int | None, int | None, str]:
        """Get the solutions and execution time for the target day's puzzles."""
        try:
            module = import_module(f"aoc2021.day_{day}.solution")
        except ModuleNotFoundError:
            return None, None, ""
        start = time()
        solution_1, solution_2 = module.compute_solution()
        timing = self._format_timing(value=time() - start)
        return solution_1, solution_2, timing

    @staticmethod
    def _format_timing(value: float) -> str:
        """Convert a time value in seconds to sensitive units."""
        if value >= 1.5 * 3600:
            return f"{value / 3600:.2f} h"
        elif value >= 1.5 * 60:
            return f"{value / 60:.2f} min"
        elif value <= 1e-3:
            return f"{value * 1e6:.2f} μs"
        elif value <= 1e-1:
            return f"{value * 1e3:.2f} ms"
        else:
            return f"{value:.2f} s"
