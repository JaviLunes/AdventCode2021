# coding=utf-8
"""Compute the solution of the Day 20: Trench Map puzzle."""

# Local application imports:
from aoc2021.common import read_puzzle_input
from aoc2021.day_20.tools import Algorithm, Image


def compute_solution() -> tuple[int, int]:
    """Compute the answers for the two parts of this day."""
    lines = read_puzzle_input(day=20)
    algorithm = Algorithm(string=lines[0])
    image = Image.from_rows(pixel_rows=lines[2:], outside_value=".")
    enhanced_image_2 = algorithm.enhance_times(image=image, times=2)
    enhanced_image_50 = algorithm.enhance_times(image=image, times=50)
    return enhanced_image_2.lit_pixels, enhanced_image_50.lit_pixels
