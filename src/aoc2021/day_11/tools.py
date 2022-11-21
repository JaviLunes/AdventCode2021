# coding=utf-8
"""Tools used for solving the Day 11: Dumbo Octopus puzzle."""

# Standard library imports:
from collections.abc import Iterable

# Third party imports:
import numpy


class Octopus:
    """Bioluminescent dumbo octopus."""
    def __init__(self, energy: int):
        self.energy = energy
        self.flashes = 0

    def __repr__(self) -> str:
        return str(self.energy)

    def be_charged(self):
        """Receive a unit of energy charge."""
        self.energy += 1

    def flash_if_possible(self) -> bool:
        """Attempt to flash, and return True/False if flashed / didn't flash."""
        if self.is_undercharged:
            return False
        self.flashes += 1
        self.energy = numpy.nan
        return True

    def rest(self):
        """Exit the 'exhausted' mode (if active)."""
        if self.is_exhausted:
            self.energy = 0

    @property
    def is_undercharged(self) -> bool:
        """State if this Octopus is below the energy level required for flashing."""
        return not (self.energy > 9)

    @property
    def is_exhausted(self) -> bool:
        """State if this Octopus is currently exhausted."""
        return numpy.isnan(self.energy)


class OctopusGroup:
    """2D grid of neatly arranged bioluminescent dumbo octopuses."""
    def __init__(self, energy_levels: numpy.ndarray):
        octopus = [Octopus(energy=e) for e in energy_levels.flat]
        self.array = numpy.array(octopus).reshape(energy_levels.shape)

    @classmethod
    def from_strings(cls, row_strings: list[str]) -> "OctopusGroup":
        """Create a new OctopusGroup from strings defining the levels of each row."""
        energy_levels = numpy.array([list(map(int, row)) for row in row_strings])
        return OctopusGroup(energy_levels=energy_levels.astype(float))

    def live_for(self, steps: int):
        """Make the provided number of steps."""
        [self._live_step() for _ in range(steps)]

    def live_until_synchronicity(self) -> int:
        """Keep making steps until the first time when all Octopus flash."""
        step = 0
        while not self.synchronous_flash:
            step += 1
            self._live_step()
        return step

    def _live_step(self):
        """Make one step, computing new energy levels and registering new flashes."""
        # Daily free charge for all octopus:
        [octo.be_charged() for octo in self.array.flat]
        # Iterate over all octopus until all are exhausted can't flash:
        while not self._all_done():
            for (i, j), octopus in numpy.ndenumerate(self.array):
                # Attempt to flash:
                if not octopus.flash_if_possible():
                    continue
                # Charge neighbours with the flash:
                for i_n, j_n in self._get_neighbours(i=i, j=j):
                    self.array[i_n, j_n].be_charged()
        # Allow exhausted octopus to rest:
        [octo.rest() for octo in self.array.flat]

    def _all_done(self) -> bool:
        """True when all octopus are exhausted or undercharged."""
        return all([
            octo.is_exhausted or octo.is_undercharged for octo in self.array.flat])

    def _get_neighbours(self, i: int, j: int) -> Iterable[tuple[int, int]]:
        """Get each Octopus adjacent to the provided coordinates."""
        x_limit, y_limit = self.array.shape
        for i_neigh in i - 1, i, i + 1:
            for j_neigh in j - 1, j, j + 1:
                if not ((0 <= i_neigh < x_limit) and (0 <= j_neigh < y_limit)):
                    continue  # Outside limits.
                if i_neigh == i and j_neigh == j:
                    continue  # Input coordinates.
                yield i_neigh, j_neigh

    @property
    def synchronous_flash(self) -> bool:
        """State if all Octopus flashed during the current step."""
        return all([octo.energy == 0 for octo in self.array.flat])

    @property
    def total_flashes(self) -> int:
        """Provide the sum of flashes emitted by all Octopus until now."""
        return sum([octo.flashes for octo in self.array.flat])
