# coding=utf-8
"""Tools used for solving the Day 18: Snailfish puzzle."""

# Standard library imports:
from itertools import permutations
from math import ceil, floor

# Third party imports:
import numpy


class SFNumber:
    """This pair ain't like your regular numbers!"""
    def __init__(self, string: str):
        self.structure = self._parse_structure(string=string)

    @staticmethod
    def _parse_structure(string: str) -> list[tuple[int, int]]:
        """Extract the internal components of a SFNumber from its value string."""
        components, current_depth, current_number = [], -1, ""
        for c, char in enumerate(string[:-1]):
            if char == "[":  # A new pair has started.
                current_depth += 1
            elif char == "]":  # The current pair has reached its end.
                current_depth -= 1
            elif char == ",":  # A pair's second half will start.
                pass
            else:  # A decimal digit: it may be a whole number, or just a part of one.
                current_number += char
                if string[c + 1] in [",", "]"]:  # Current number is completed.
                    components.append((int(current_number), current_depth))
                    current_number = ""
        return components

    @classmethod
    def from_structure(cls, structure: list[tuple[int, int]]) -> "SFNumber":
        """Build a new SFNumber directly from its structure."""
        number = SFNumber(string="")  # Not the most elegant thing...
        number.structure = structure
        return number

    def __add__(self, other: "SFNumber") -> "SFNumber":
        left = [(v, d + 1) for v, d in self.structure]
        right = [(v, d + 1) for v, d in other.structure]
        result = SFNumber.from_structure(structure=left + right)
        result.reduce()
        return result

    def __eq__(self, other: "SFNumber") -> bool:
        return self.structure == other.structure

    def __repr__(self) -> str:
        return str(self.structure)

    @property
    def magnitude(self) -> int:
        """Compute the magnitude of this SFNumber."""
        # Build a 2D representation of the structure component:
        max_depth = max(item[1] for item in self.structure)
        array = numpy.full((max_depth + 2, len(self.structure)), -1)
        # Place each component at its location and depth (+2) in the 2D map:
        for i, (value, depth) in enumerate(self.structure):
            array[depth + 1, i] = value
        # Compress each level by applying the magnitude formula pair-wise to its values:
        for d in range(max_depth + 1, 0, -1):  # From deepest to shallowest.
            magnitudes = self._compress_level(values=list(array[d, :]))
            array[d - 1, :] = numpy.maximum(array[d - 1, :], magnitudes)
        return array[0, 0]  # The last level is the total magnitude of the structure.

    @staticmethod
    def _compress_level(values: list[int]) -> tuple[int, int]:
        """Apply the 3 * a + 2 * b formula to positive values of this depth level."""
        i, values, j = 0, list(values), -1
        compressed = numpy.full(shape=(len(values)), fill_value=-1)
        for i in range(len(values)):
            if values[i] != -1:  # A positive value to compress.
                if j == -1:  # We need a second value to compress a pair.
                    compressed[i], j = values[i], i
                else:  # We have a complete pair. Compress it.
                    compressed[j], j = 3 * compressed[j] + 2 * values[i], -1
        return compressed

    def reduce(self):
        """
        Repeatedly try to explode or split this SFNumber until neither is possible.

        Exploding any pre-existent deep, pure pair (or any one generated during
        explosions or splits) takes precedence over splitting any pre-existent large
        integer (or any one generated). When no more explodes can be done, try to make
        a single split. If one is made, restart the cycle by trying to explode again.
        If no split was made, the structure is completely reduced.
        """
        while True:
            self.explode()  # Keep exploding until there are no more exploding pairs.
            if not self.split():  # If a split is made, there may be new exploding pairs.
                break  # All possible explodes and splits are done.

    def explode(self) -> None:
        """Replace ALL 4-deep-pairs of pure integers by 0s and propagate their values."""
        for i_l in range(len(self.structure) - 1):
            i_r = i_l + 1
            value_l, depth_l = self.structure[i_l]
            value_r, depth_r = self.structure[i_r]
            # Ignore if non-pure or too shallow pair:
            if (depth_l != depth_r) or (depth_l < 4):
                continue
            # Propagate left value towards left (if possible):
            i_prev = i_l - 1
            while i_prev >= 0:
                if self.structure[i_prev] == (-1, -1):
                    i_prev -= 1  # Worry about previous items marked for deletion!
                else:
                    value_prev, depth_prev = self.structure[i_prev]
                    self.structure[i_prev] = (value_prev + value_l, depth_prev)
                    break
            # Propagate right value towards right (if possible):
            if i_r < len(self.structure) - 1:
                value_next, depth_next = self.structure[i_r + 1]
                self.structure[i_r + 1] = (value_next + value_r, depth_next)
            # Update structure:
            self.structure[i_l] = (-1, -1)  # Marked for future deletion.
            self.structure[i_r] = (0, depth_r - 1)  # Remains of explosion.
        # Remove marked items:
        self.structure = list(filter(lambda i: i != (-1, -1), self.structure))

    def split(self) -> bool:
        """Replace FIRST integer > 9 by a pair with its floor and cell divisions by 2."""
        for i, (value, depth) in enumerate(self.structure):
            if value > 9:  # Large integer. Split it!
                # Split the value and build the two new items:
                left_split = floor(value / 2)
                right_split = ceil(value / 2)
                new_items = [(left_split, depth + 1), (right_split, depth + 1)]
                # Insert new items at the proper location:
                self.structure = self.structure[:i] + new_items + self.structure[i + 1:]
                return True  # Stop looking for more integers to split.
        return False


class Homework:
    """A sequence of SFNumber objects to add together."""
    def __init__(self, number_strings: list[str]):
        self.numbers = [SFNumber(string=string) for string in number_strings]

    def sum(self) -> SFNumber:
        """Compute the sum of all stored SFNumber objects."""
        a = self.numbers[0]
        for b in self.numbers[1:]:
            a += b
        return a

    def find_total_magnitude(self) -> int:
        """Compute the magnitude of the sum of all stored SFNumber objects."""
        sum_number = self.sum()
        return sum_number.magnitude

    def find_max_twofold_magnitude(self) -> int:
        """Compute the max magnitude achievable by summing two of the stored numbers."""
        sums = [a + b for a, b in permutations(self.numbers, r=2)]
        return max(number.magnitude for number in sums)
