# coding=utf-8
"""Shared tools used across different daily puzzles."""

# Standard library imports:
from pathlib import Path

# Set constants:
BASE_PATH = Path(__file__).parent


def read_puzzle_input(day: int) -> list[str]:
    """Read, process and return each line in the input file for the target day."""
    file_path = BASE_PATH / f"day_{day}" / "puzzle_input.txt"
    with open(file_path, mode="r") as file:
        lines = [line.removesuffix("\n") for line in file]
    return lines
