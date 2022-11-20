# coding=utf-8
"""Tools used for solving the Day 9: Smoke Basin puzzle."""

# Third party imports:
import numpy


class Cave:
    """Cell representation of a lava tube cave system, storing cell height data."""
    def __init__(self, heights_array: numpy.ndarray, wall_height: int = 20):
        self.wall_height = wall_height
        self.map = heights_array

    @classmethod
    def from_row_strings(cls, height_rows: list[str], wall_height: int = 20) -> "Cave":
        """Build a new Cave from a list of strings, each containing heights per row."""
        shape = len(height_rows) + 2, len(height_rows[0]) + 2
        height_map = numpy.full(shape=shape, fill_value=wall_height)
        for r, row in enumerate(height_rows):
            height_map[r + 1, 1:-1] = list(map(int, [*row]))
        return Cave(heights_array=height_map, wall_height=wall_height)

    def explore(self, i_start: int, j_start, impassable_height: int = None) -> "Cave":
        """Build a Cave from all cells reachable without crossing impassable heights."""
        if impassable_height is None:
            impassable_height = self.wall_height
        assert 0 < impassable_height <= self.wall_height,  "Invalid impassable height!"
        charted_map = numpy.where(self.map < impassable_height, 0, 2)
        # If we start at an impassable height, no exploration is done:
        if numpy.isnan(charted_map[i_start, j_start]):
            return charted_map
        # Explore uncharted cells:
        uncharted_cells = [[i_start, j_start]]
        while uncharted_cells:
            i, j = uncharted_cells.pop(0)
            charted_map[i, j] = 1
            # Check if adjacent cells are reachable:
            for next_i, next_j in [i - 1, j], [i + 1, j], [i, j - 1], [i, j + 1]:
                if charted_map[next_i, next_j] == 0:
                    uncharted_cells.append([next_i, next_j])
        heights_map = numpy.where(charted_map == 1, self.map, impassable_height)
        return Cave(heights_array=heights_map, wall_height=impassable_height)

    def explore_basins(self, impassable_height: int = None) -> list["Cave"]:
        """Starting from each local low point, make all possible explorations."""
        return [self.explore(i_start=i, j_start=j, impassable_height=impassable_height)
                for i, j in zip(*numpy.nonzero(~numpy.isnan(self.local_lows)))]

    @property
    def size(self) -> int:
        """Provide the number of non-wall cells in this Cave."""
        return int((self.map < self.wall_height).sum())

    @property
    def local_lows(self) -> numpy.array:
        """Show the height of each local low point, masking other points to NaN."""
        desc_x1 = (self.map[1:, :] - self.map[:-1, :])[:-1, 1:-1] < 0
        desc_x2 = (self.map[:-1, :] - self.map[1:, :])[1:, 1:-1] < 0
        desc_y1 = (self.map[:, 1:] - self.map[:, :-1])[1:-1, :-1] < 0
        desc_y2 = (self.map[:, :-1] - self.map[:, 1:])[1:-1, 1:] < 0
        cave_mask = numpy.full(shape=self.map.shape, fill_value=False)
        cave_mask[1:-1, 1:-1] = desc_x1 & desc_x2 & desc_y1 & desc_y2
        return numpy.where(cave_mask, self.map, numpy.nan)

    @property
    def total_local_lows(self) -> int:
        """Provide the total number of local low points."""
        return int(self.map.size - numpy.isnan(self.local_lows).sum())

    @property
    def total_risk_level(self) -> int:
        """Provide the total risk level for all local low points."""
        return int(numpy.nansum(self.local_lows + 1))
