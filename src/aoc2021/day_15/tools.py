# coding=utf-8
"""Tools used for solving the Day 15: Chiton puzzle."""

# Standard library imports:
from collections.abc import Iterable
import heapq
from itertools import product

# Third party imports:
import numpy


class Node:
    """Individual cave cell storing location, and g and h costs for A* search."""
    def __init__(self, i: int, j: int, g: int = numpy.Inf):
        self.i = i
        self.j = j
        self.g = g  # Total cost of moving from start to this Node's location

    def __lt__(self, other: "Node") -> bool:
        # Note: Only compare nodes' g costs to optimize min heap sorting speed.
        return self.g < other.g

    @property
    def location(self) -> tuple[int, int]:
        """Provide the X-Y coordinates of this Node."""
        return self.i, self.j

    def get_f(self, goal: tuple[int, int], h_metric: str = "Manhattan") -> int:
        """Compute the estimated cost of moving from start to goal through this Node."""
        return self.g + self.get_h(goal=goal, h_metric=h_metric)

    def get_h(self, goal: tuple[int, int], h_metric: str = "Manhattan") -> int:
        """Give an educated guess for the cost of moving from this Node to goal."""
        if h_metric.lower() == "manhattan":  # Manhattan distance.
            return abs(self.i - goal[0]) + abs(self.j - goal[1])
        elif h_metric.lower() == "ignore":  # Do not try to guess h; all locations get 0.
            return 0
        else:
            raise ValueError(f"'{h_metric}' is not a valid estimation metric.")


class ChironCave:
    """2D, square-shaped cave with walls densely covered by dangerous mollusks."""
    def __init__(self, risk_levels: list[str], start: tuple[int, int] = (0, 0),
                 goal: tuple[int, int] = None):
        self.risk_map = self._build_risk_map(risk_levels=risk_levels)
        self.start = start
        self.goal = goal if goal is not None else self._get_default_goal()

    def _build_risk_map(self, risk_levels) -> numpy.ndarray:
        """Create a quadrangular 2D map of individual risk values."""
        shape = (len(risk_levels), len(risk_levels[0]))
        return numpy.array(list(map(int, "".join(risk_levels)))).reshape(shape)

    def _get_default_goal(self) -> tuple[int, int]:
        """Provide a default goal at the rightmost-bottom corner."""
        return self.risk_map.shape[0] - 1, self.risk_map.shape[1] - 1

    def get_minimum_total_risk(self, include_start: bool) -> int:
        """Use an A* search algorithm to find the path with least chiron crash risk."""
        # Build lists / queues / min heaps / sets / cost maps:
        pending_nodes = []
        visited_nodes = set()
        ijs = product(range(self.risk_map.shape[0]), range(self.risk_map.shape[1]))
        best_g_costs = dict({(i, j): numpy.Inf for i, j in ijs})
        # Prepare starting node:
        q_node = Node(i=self.start[0], j=self.start[1], g=self.risk_map[self.start])
        pending_nodes.append(q_node)
        best_g_costs[q_node.location] = q_node.g
        # Check each pending Node one at a time, from lowest to greatest g cost:
        while pending_nodes:
            q_node = heapq.heappop(pending_nodes)
            # Stop if the goal is reached:
            if q_node.location == self.goal:
                q_f = q_node.get_f(goal=self.goal, h_metric="Manhattan")
                return q_f - (0 if include_start else self.risk_map[self.start])
            if q_node.location in visited_nodes:
                continue  # Skip node if its location was already visited.
            # For each possible direction of movement (potential future Node to check):
            for s_node in self._get_successors(node=q_node):
                if s_node.location in visited_nodes:
                    continue  # Skip successor if its location was already visited.
                if s_node.g >= best_g_costs[s_node.location]:
                    continue  # Skip successor if worse than its location's best cost.
                # Register successor Node for future checking:
                heapq.heappush(pending_nodes, s_node)
                best_g_costs[s_node.location] = s_node.g
            # Register the q Node's location as already seen:
            visited_nodes.add(q_node.location)

    def _get_successors(self, node: Node) -> Iterable[Node]:
        """Return all possible neighbour Nodes of the provided Node."""
        i, j, shape = node.i, node.j, self.risk_map.shape
        for ii, jj in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
            if (0 <= ii < shape[0]) and (0 <= jj < shape[1]):
                yield Node(i=ii, j=jj, g=node.g + self.risk_map[ii, jj])


class ExpandedChironCave(ChironCave):
    """Tile-expanded 2D cave with even more walls filled with dangerous mollusks."""
    def _build_risk_map(self, risk_levels) -> numpy.ndarray:
        """Create a quadrangular 2D map of individual risk values."""
        base_tile = super()._build_risk_map(risk_levels=risk_levels)
        return self._expand_map(risk_map=base_tile)

    @staticmethod
    def _expand_map(risk_map: numpy.ndarray) -> numpy.ndarray:
        """Build a bigger map by expanding the original risk map into a 5 x 5 tile set."""
        tile_x, tile_y = risk_map.shape
        big_map = numpy.zeros(shape=(tile_x * 5, tile_y * 5), dtype=int)
        big_map[:tile_x, :tile_y] = risk_map
        # Rightwards expansion of original tile:
        for t in range(4):
            base_sub = slice(t * tile_x, (t + 1) * tile_x), slice(0, tile_y)
            new_sub = slice((t + 1) * tile_x, (t + 2) * tile_x), slice(0, tile_y)
            big_map[new_sub] = numpy.where(
                big_map[base_sub] == 9, 1, big_map[base_sub] + 1)
        # Downwards expansion of first row of tiles:
        for t in range(4):
            base_sub = slice(0, tile_x * 5), slice(t * tile_y, (t + 1) * tile_y)
            new_sub = slice(0, tile_x * 5), slice((t + 1) * tile_y, (t + 2) * tile_y)
            big_map[new_sub] = numpy.where(
                big_map[base_sub] == 9, 1, big_map[base_sub] + 1)
        return big_map
