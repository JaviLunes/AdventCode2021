# coding=utf-8
"""Tools used for solving the Day 6: Lanternfish puzzle."""

# Standard library imports:
from collections import Counter


class School:
    """Group of memory-aware lanternfish individuals."""
    def __init__(self, fish_states: list[int]):
        self.school = self._classify_fishes(fish_states=fish_states)

    @staticmethod
    def _classify_fishes(fish_states: list[int]) -> tuple[int, ...]:
        """Group and count fishes by their state value into a tuple."""
        counter = Counter(fish_states)
        return tuple(counter.get(i, 0) for i in range(9))

    def live_for(self, days: int):
        """Make the provided number of days pass."""
        [self._live_day() for _ in range(days)]

    def _live_day(self):
        """All fishes in the school live a new day."""
        updated_school = (
            self.school[1],                     # Group 0: old group 1
            self.school[2],                     # Group 1: old group 2
            self.school[3],                     # Group 2: old group 3
            self.school[4],                     # Group 3: old group 4
            self.school[5],                     # Group 4: old group 5
            self.school[6],                     # Group 5: old group 6
            self.school[7] + self.school[0],    # Group 6: old groups 7 and 0
            self.school[8],                     # Group 7: old group 8
            self.school[0])                     # Group 8: newborns
        self.school = updated_school

    @property
    def active_fishes(self) -> int:
        """Provide the number of fishes currently living in this School."""
        return sum(self.school)
