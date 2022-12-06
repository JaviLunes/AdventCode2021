# coding=utf-8
"""Tools used for solving the Day 19: Beacon Scanner puzzle."""

# Standard library imports:
from typing import Union

# Third party imports:
import numpy


class Point:
    """Coordinates describing a 3D location (or a distance to a reference Point)."""
    __slots__ = ["x", "y", "z"]

    def __init__(self, x: int, y: int, z: int):
        self.x, self.y, self.z = x, y, z

    def __repr__(self) -> str:
        return f"({self.x},{self.y},{self.z})"

    def __add__(self, other: "Point") -> "Point":
        return Point(x=self.x + other.x, y=self.y + other.y, z=self.z + other.z)

    def __sub__(self, other: "Point") -> "Point":
        return Point(x=self.x - other.x, y=self.y - other.y, z=self.z - other.z)

    def __eq__(self, other: "Point") -> bool:
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

    @property
    def coordinates(self) -> tuple[int, int, int]:
        """Provide a tuple with the coordinates of this Point."""
        return self.x, self.y, self.z


class Scanner:
    """Underwater scanner able to detect beacons within 1000 units in a 3D region."""
    def __init__(self, name: str, beacons: list[Point]):
        self.name = name
        self.beacons = beacons
        self.origin = Point(x=0, y=0, z=0)
        self.rotation = None  # TODO...

    @classmethod
    def from_str(cls, name: str, beacons: list[str]) -> "Scanner":
        """Create a new Scanner object by parsing strings representing beacons."""
        beacons = [Point(*map(int, beacon.split(","))) for beacon in beacons]
        return Scanner(name=name, beacons=beacons)


class ScannerAligner:
    """Tool for finding the common rotation and alignment shift between Scanner pairs."""
    def __init__(self, minimum_shared_beacons: int):
        self._min_beacons = minimum_shared_beacons

    def align_to_reference(self, target: Scanner, ref: Scanner) -> None:
        """Try to align a target Scanner with another reference Scanner."""
        distance_array = self._compute_beacon_distances(a=target, b=ref)
        shift = self._find_common_distance(dist_array=distance_array)
        if shift is None:
            raise ValueError("These two Scanner objects can't be aligned.")
        target.origin = shift

    def align_rotation(self, target: Scanner, ref: Scanner):
        """Try to align one of the rotations of a Scanner with another reference."""
        rotations = ...  # TODO: Generate the 24 (?) rotation Scanners of 'aligned'
        for rotation, rotated_target in rotations:
            try:
                self.align_to_reference(target=rotated_target, ref=ref)
            except ValueError:
                continue
            else:
                target.origin = rotated_target.origin
                target.rotation = rotation
        raise ValueError("These two Scanner objects can't be aligned!")

    @staticmethod
    def _compute_beacon_distances(a: Scanner, b: Scanner) -> numpy.ndarray:
        """Generate an array of distances between beacons of two Scanner objects."""
        m, n = len(b.beacons), len(a.beacons)
        distances = (b.beacons[i] - a.beacons[j] for i in range(m) for j in range(n))
        return numpy.fromiter(distances, dtype=object).reshape((m, n))

    def _find_common_distance(self, dist_array: numpy.ndarray) -> Union["Point", None]:
        """Return first array's distance repeated in a min quantity of rows and cols."""
        unique_distances = {*dist_array.flatten()}
        if len(unique_distances) == numpy.product(dist_array.shape):
            return None  # There are no duplicated distances.
        row_sets = [{*dist_array[i, :].flatten()} for i in range(dist_array.shape[0])]
        col_sets = [{*dist_array[:, j].flatten()} for j in range(dist_array.shape[1])]
        for dist in unique_distances:
            row_matches = sum(dist in row for row in row_sets)
            col_matches = sum(dist in col for col in col_sets)
            if row_matches >= self._min_beacons and col_matches >= self._min_beacons:
                return dist
        return None
