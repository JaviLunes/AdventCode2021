# coding=utf-8
"""Tools used for solving the Day 12: Passage Pathing puzzle."""

# Standard library imports:
from collections import Counter


class Cave:
    """Individual node with a name, a size, and connections to other neighbour nodes."""
    def __init__(self, name: str):
        self.name = name
        self.neighbours = []

    def __repr__(self) -> str:
        connections = "|".join(cave.name for cave in self.neighbours)
        return f"{self.name} -> {connections or '-'}"

    def connect_to(self, cave: "Cave"):
        """Register another Cave object as connected to this Cave."""
        self.neighbours.append(cave)

    @property
    def is_small(self) -> bool:
        """State whether this cave is small (True) or big (False)."""
        return self.name.lower() == self.name


class CavePath:
    """Sequence of Cave nodes forming a path (hopefully towards an 'end' Cave)."""
    def __init__(self, previous_path: list[Cave] = None):
        self.path = [] if previous_path is None else [*previous_path]

    def __repr__(self) -> str:
        return "->".join(cave.name for cave in self.path)

    def expand_path(self, cave: Cave) -> list:
        """Create new CavePath objects by appending viable neighbour Caves."""
        # Add provided cave:
        self.path.append(cave)
        # Finish exploration if complete:
        if self.is_complete:
            return [self]
        # Keep exploring into cave neighbours:
        bifurcations = []
        for neighbour in cave.neighbours:
            child_path = self.__class__(previous_path=self.path)
            bifurcations.extend(child_path.expand_path(cave=neighbour))
        return bifurcations

    @property
    def is_complete(self) -> bool:
        """True if end is reached or a small cave is repeated, False elsewhere."""
        if self.reached_end:
            return True
        if self.reached_start_again:
            return True
        if not self.reached_small:
            return False  # Big cave: Don't bother checking previous caves.
        if self.reached_small_twice:
            return True
        return False

    @property
    def reached_end(self) -> bool:
        """Check if the exploration has reached an 'end' Cave."""
        return self.path[-1].name == "end"

    @property
    def reached_start_again(self) -> bool:
        """Check if the exploration has returned to an 'start' Cave."""
        return self.path[-1].name == "start" and len(self.path) > 1

    @property
    def reached_small(self) -> bool:
        """Check if the exploration has reached a small Cave."""
        return self.path[-1].name.lower() == self.path[-1].name

    @property
    def reached_small_twice(self) -> bool:
        """Check if the exploration has reached the same small Cave twice."""
        return self.path[-1].name in [c.name for c in self.path[:-2]]


class RelaxedCavePath(CavePath):
    """Sequence of Cave nodes forming a path (hopefully towards an 'end' Cave)."""
    @property
    def reached_small_twice(self) -> bool:
        """Now at most one small cave can be reached twice (and no more)."""
        visits = Counter(c.name for c in self.path if c.is_small and c.name != "start")
        if [v for v in visits.values() if v > 2]:
            return True  # Any small cave visited more than two times.
        if len([v for v in visits.values() if v == 2]) > 1:
            return True  # More than one small cave visited twice.
        return False


class CaveSystem:
    """Set of unique Cave nodes."""
    def __init__(self, caves: dict[str, Cave]):
        self.caves = caves

    @classmethod
    def from_paths(cls, paths: list[str]) -> "CaveSystem":
        """Create a CaveSystem object from a collection of cave path strings."""
        caves = {name: Cave(name=name) for name in set("-".join(paths).split("-"))}
        for path in paths:
            name_1, name_2 = path.split("-")
            caves[name_1].connect_to(cave=caves[name_2])
            caves[name_2].connect_to(cave=caves[name_1])
        return CaveSystem(caves=caves)

    def compute_valid_paths(self) -> list[CavePath]:
        """Generate all possible valid paths moving from start to end."""
        completed_paths = CavePath().expand_path(cave=self.caves["start"])
        return list(filter(lambda path: path.reached_end, completed_paths))

    def compute_relaxed_paths(self) -> list[RelaxedCavePath]:
        """Generate all possible valid paths moving from start to end."""
        completed_paths = RelaxedCavePath().expand_path(cave=self.caves["start"])
        return list(filter(lambda path: path.reached_end, completed_paths))
