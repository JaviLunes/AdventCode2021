# coding=utf-8
"""Tools used for solving the Day 5: Hydrothermal Venture puzzle."""

# Standard library imports:
from typing import Iterable

# Third party imports:
import numpy


class Point:
    """2D point."""
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"({self.x},{self.y})"

    @classmethod
    def from_str(cls, string: str) -> "Point":
        """Create a Point by parsing an 'x,y' formatted string."""
        x, y = string.replace(" ", "").split(",")
        return Point(x=int(x), y=int(y))


class VentMap:
    """2D map marking the location and number of hydrothermal vent lines."""
    def __init__(self, vent_segments: list[str], diagonals: bool):
        points = list(self._vectors_to_points(vectors=vent_segments, diagonals=diagonals))
        self._build_map(points=points)
        self._populate_map(points=points)

    def _vectors_to_points(self, vectors: list[str], diagonals: bool) -> Iterable[Point]:
        """Transform linear vectors into groups of 2D points crossed by them."""
        for vector in vectors:
            start, end = self._vector_to_limits(vector=vector)
            for point in self._limits_to_points(
                    start=start, end=end, diagonals=diagonals):
                yield point

    @staticmethod
    def _vector_to_limits(vector: str) -> tuple[Point, Point]:
        """Transform a linear vector into their starting and ending 2D points."""
        start, end = vector.split(" -> ")
        return Point.from_str(string=start), Point.from_str(string=end)

    @staticmethod
    def _limits_to_points(start: Point, end: Point, diagonals: bool) -> Iterable[Point]:
        """Build a list of crossed points from a pair of starting and ending points."""
        sign_x, sign_y = numpy.sign(end.x - start.x), numpy.sign(end.y - start.y)
        range_x = range(start.x, end.x + sign_x, sign_x or 1)
        range_y = range(start.y, end.y + sign_y, sign_y or 1)
        if len(range_x) > 0 and len(range_y) == 0:  # X-line:
            return (Point(x=x, y=start.y) for x in range_x)
        elif len(range_x) == 0 and len(range_y) > 0:  # Y-line:
            return (Point(x=start.x, y=y) for y in range_y)
        elif len(range_x) == len(range_y) and diagonals:  # Diagonal line:
            return (Point(x=x, y=y) for x, y in zip(range_x, range_y))
        else:  # Ignored line:
            return []

    def _build_map(self, points: list[Point]):
        """Build a 2D map sized to contain all provided vent points."""
        max_x = max(points, key=lambda point: point.x)
        max_y = max(points, key=lambda point: point.y)
        self.map = numpy.zeros((max_x.x + 1, max_y.y + 1)).T

    def _populate_map(self, points: list[Point]):
        """Mark all vent points in the 2D map."""
        for point in points:
            self.map[point.y, point.x] += 1  # The axis of the map are [Y, X]

    @property
    def dangerous_points(self) -> list[Point]:
        """Provide a list of locations where multiple vent lines converge."""
        xs, ys = list(map(lambda a: a.tolist(), numpy.where(self.map > 1)))
        return [Point(x=x, y=y) for x, y in zip(xs, ys)]
