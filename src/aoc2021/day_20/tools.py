# coding=utf-8
"""Tools used for solving the Day 20: Trench Map puzzle."""

# Standard library imports:
from collections.abc import Iterable

# Third party imports:
import numpy


class Image:
    """Infinite-size, pixelated image sent by the constellation of submarine scanners."""
    def __init__(self, pixel_array: numpy.ndarray, outside_value: str):
        self.pixels = pixel_array
        self.out_value = outside_value
        self._trim_borders()

    def __eq__(self, other: "Image") -> bool:
        return numpy.array_equal(self.pixels, other.pixels)

    def _trim_borders(self):
        """Reduce the image size by cutting out borders without lit pixels."""
        lit_rows = [i for i in range(self.shape[0]) if any(self.pixels[i, :])]
        lit_cols = [j for j in range(self.shape[1]) if any(self.pixels[:, j])]
        a = slice(lit_rows[0], lit_rows[-1] + 1) if lit_rows else slice(self.shape[0])
        b = slice(lit_rows[0], lit_cols[-1] + 1) if lit_cols else slice(self.shape[1])
        self.pixels = self.pixels[a, b]

    @property
    def shape(self) -> tuple[int, int]:
        """Provide the width and height in pixels of this Image."""
        return self.pixels.shape

    @property
    def lit_pixels(self) -> int:
        """Count the number of '#' pixels in this Image."""
        return self.pixels.sum()

    def get_pixel(self, x: int, y: int) -> str:
        """Provide the value of the pixel located at the provided coordinates."""
        if (0 <= x < self.shape[0]) and (0 <= y < self.shape[1]):
            return "#" if self.pixels[(y, x)] else "."
        return self.out_value

    def get_pixel_grid(self, x: int, y: int) -> list[str]:
        """Provide the values of the 3x3 pixel grid centered at the provided location."""
        pixels = [(x + dx, y + dy) for dy in [-1, 0, 1] for dx in [-1, 0, 1]]
        return [self.get_pixel(x=x, y=y) for x, y in pixels]

    @classmethod
    def from_iterable(
            cls, *values: str, shape: tuple[int, int], outside_value: str) -> "Image":
        """Create a new Image from a sequence of '.' and '#' characters and a shape."""
        boolean_iter = (char == "#" for char in values)
        data = numpy.fromiter(boolean_iter, dtype=bool).reshape(shape)
        return cls(pixel_array=data, outside_value=outside_value)

    @classmethod
    def from_rows(cls, pixel_rows: list[str], outside_value: str) -> "Image":
        """Create a new Image from a group of strings containing '.' and '#' chars."""
        shape = len(pixel_rows), len(pixel_rows[0])
        values = "".join(pixel_rows)
        return cls.from_iterable(*values, shape=shape, outside_value=outside_value)

    @staticmethod
    def _parse_binary_string(string: str) -> Iterable[bool]:
        """Convert a string of '.' and '#' characters into an iterable of booleans."""
        return map(lambda char: char == "#", string)


class Algorithm:
    """Enhancement algorithm able to increase the pixel resolution of an Image."""
    def __init__(self, string: str):
        self._code_map = string

    def enhance_times(self, image: Image, times: int) -> Image:
        """Increase an Image's pixel resolution multiple times."""
        for _ in range(times):
            image = self.enhance(image=image)
        return image

    def enhance(self, image: Image) -> Image:
        """Apply the internal value map to increase an Image's pixel resolution."""
        locations = list(self._get_target_locations(image=image))
        pixel_grid_strings = [self._read_grid(image=image, pixel=p) for p in locations]
        pixel_codes = [self._encode_grid_string(string=s) for s in pixel_grid_strings]
        pixel_values = [self._code_map[c] for c in pixel_codes]
        enhanced_shape = image.shape[0] + 2, image.shape[1] + 2
        outside_value = self._update_outside_value(image=image)
        return Image.from_iterable(
            *pixel_values, shape=enhanced_shape, outside_value=outside_value)

    @staticmethod
    def _get_target_locations(image: Image) -> Iterable[tuple[int, int]]:
        """Get the locations of the pixels for a new, enhanced Image."""
        i_range = range(-1, image.shape[0] + 1)
        j_range = range(-1, image.shape[1] + 1)
        return ((i, j) for j in j_range for i in i_range)

    @staticmethod
    def _read_grid(image: Image, pixel: tuple[int, int]) -> str:
        """Read and combine the values of a 3x3 pixel grid centered in a target pixel."""
        return "".join(image.get_pixel_grid(x=pixel[0], y=pixel[1]))

    @staticmethod
    def _encode_grid_string(string: str) -> int:
        """Transform a '.'|'#' string from a 3x3 pixel grid into a decimal number."""
        return int("".join(str(int(char == "#")) for char in string), 2)

    def _update_outside_value(self, image: Image) -> str:
        """Compute the outside-borders value for the enhanced version of an Image. """
        outside_grid = "".join([image.out_value] * 9)
        outside_code = self._encode_grid_string(string=outside_grid)
        return self._code_map[outside_code]
