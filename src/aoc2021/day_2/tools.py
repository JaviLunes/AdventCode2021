# coding=utf-8
"""Tools used for solving the Day 2: Dive! puzzle."""


class Submarine:
    """Define a moving submarine."""
    def __init__(self):
        self.horizontal = 0
        self.depth = 0

    def implement_course(self, course: list[tuple, int]):
        """Execute all movement instructions defined in the provided course."""
        for direction, distance in course:
            self._move(direction=direction, distance=distance)

    def _move(self, direction: str, distance: int):
        """Move the submarine a certain distance in the provided direction."""
        if direction == "forward":
            self.horizontal += distance
        elif direction == "down":
            self.depth += distance
        elif direction == "up":
            self.depth -= distance
        else:
            raise ValueError(f"Unrecognized '{direction}' direction")

    @property
    def total_movement(self) -> int:
        """Compute the combination of horizontal and diving movement."""
        return self.horizontal * self.depth


class AimSubmarine(Submarine):
    """Define a Submarine that uses aim for movement."""
    def __init__(self):
        super().__init__()
        self.aim = 0

    def _move(self, direction: str, distance: int):
        """Move the submarine a certain distance in the provided direction."""
        if direction == "forward":
            self.horizontal += distance
            self.depth += distance * self.aim
        elif direction == "down":
            self.aim += distance
        elif direction == "up":
            self.aim -= distance
        else:
            raise ValueError(f"Unrecognized '{direction}' direction")
