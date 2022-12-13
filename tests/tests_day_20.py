# coding=utf-8
"""Tests for the Day 20: Trench Map puzzle."""

# Standard library imports:
from pathlib import Path
import unittest

# Local application imports:
from aoc2021.day_20.tools import Algorithm, Image

# Set constants:
DATA_PATH = Path(__file__).parent / "data" / "day_20"


class ExampleTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        lines_input = self._load_data(file_name="example_input.txt")
        lines_1 = self._load_data(file_name="example_enhanced_1.txt")
        lines_2 = self._load_data(file_name="example_enhanced_2.txt")
        self.algorithm = Algorithm(string=lines_input[0])
        self.image_input = Image.from_rows(pixel_rows=lines_input[2:], outside_value=".")
        self.image_1 = Image.from_rows(pixel_rows=lines_1, outside_value=".")
        self.image_2 = Image.from_rows(pixel_rows=lines_2, outside_value=".")

    @staticmethod
    def _load_data(file_name: str) -> list[str]:
        """Extract all lines from text files."""
        with open(DATA_PATH / file_name, mode="r") as file:
            lines = [line.removesuffix("\n") for line in file]
        return lines

    def test_pixel_to_code(self):
        """The 9 pixels centered at the Image middle point codify the number 34."""
        grid_string = self.algorithm._read_grid(image=self.image_input, pixel=(2, 2))
        self.assertEqual(34, self.algorithm._encode_grid_string(string=grid_string))

    def test_enhance_image_once(self):
        """The example Image 1 is the result of enhancing once the example Image 0."""
        enhanced_image = self.algorithm.enhance_times(image=self.image_input, times=1)
        self.assertEqual(self.image_1, enhanced_image)

    def test_enhance_image_twice(self):
        """The example Image 2 is the result of enhancing twice the example Image 0."""
        enhanced_image = self.algorithm.enhance_times(image=self.image_input, times=2)
        self.assertEqual(self.image_2, enhanced_image)

    def test_lit_pixels_of_twice_enhanced_image(self):
        """The number of lit pixels after enhancing twice the input image is 35."""
        enhanced_image = self.algorithm.enhance_times(image=self.image_input, times=2)
        self.assertEqual(35, enhanced_image.lit_pixels)

    def test_lit_pixels_of_50_enhanced_image(self):
        """The number of lit pixels after enhancing 50 times the input image is 3351."""
        enhanced_image = self.algorithm.enhance_times(image=self.image_input, times=50)
        self.assertEqual(3351, enhanced_image.lit_pixels)
