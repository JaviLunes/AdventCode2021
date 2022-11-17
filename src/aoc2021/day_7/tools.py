# coding=utf-8
"""Tools used for solving the Day 7: The Treachery of Whales puzzle."""


class Crab:
    """Define a crab (and its tiny submarine), able to move only horizontally."""
    def __init__(self, position: int):
        self.position = position

    def compute_linear_cost(self, new_position: int) -> int:
        """Calculate the fuel needed for moving this Crab to a new position."""
        return abs(new_position - self.position)

    def compute_triangular_cost(self, new_position: int) -> int:
        """Calculate the fuel needed for moving this Crab to a new position."""
        movements = abs(new_position - self.position)
        return int(movements * (movements + 1) / 2)


class CrabSwarm:
    """Define a swarm of Crab objects."""
    def __init__(self, crabs: list[Crab]):
        self._crabs = [*crabs]

    def minimize_cost(self, linear: bool) -> tuple[int, int]:
        """Calculate the position with the least fuel consumption for the swarm."""
        min_position = min(crab.position for crab in self._crabs)
        max_position = max(crab.position for crab in self._crabs)
        position_range = range(min_position, max_position + 1)
        if linear:
            cost_options = {
                p: self._get_linear_cost(new_position=p) for p in position_range}
        else:
            cost_options = {
                p: self._get_triangular_cost(new_position=p) for p in position_range}
        optimum = min(cost_options.items(), key=lambda x: x[1])
        return optimum

    def _get_linear_cost(self, new_position: int) -> int:
        """Calculate the fuel needed for moving all the swarm to a new position."""
        return sum(crab.compute_linear_cost(new_position=new_position)
                   for crab in self._crabs)

    def _get_triangular_cost(self, new_position: int) -> int:
        """Calculate the fuel needed for moving all the swarm to a new position."""
        return sum(crab.compute_triangular_cost(new_position=new_position)
                   for crab in self._crabs)
