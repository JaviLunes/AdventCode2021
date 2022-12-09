# coding=utf-8
"""Tools used for solving the Day 19: Beacon Scanner puzzle."""

# Standard library imports:
from itertools import chain, permutations
from typing import Iterable, Union

# Third party imports:
import numpy
from scipy.spatial.transform import Rotation


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
        """Provide the coordinates of this Point as a tuple."""
        return self.x, self.y, self.z

    def rotate(self, rotation: Rotation) -> "Point":
        """Build a new Point object by applying a scipy.Rotation to this Point."""
        return Point(*map(round, rotation.apply([self.x, self.y, self.z])))

    def distance(self, other: "Point") -> int:
        """Compute the Manhattan distance between this and another Point."""
        return sum(abs(b - a) for a, b in zip(self.coordinates, other.coordinates))


class Scanner:
    """Underwater scanner able to detect beacons within 1000 units in a 3D region."""
    def __init__(self, beacons: list[Point], i: int = -1):
        self.i = i
        self._beacons = list(set(beacons))
        self.origin = Point(x=0, y=0, z=0)

    def __repr__(self) -> str:
        return f"Scanner {self.i} {self.origin}"

    def __add__(self, other: "Scanner") -> "Scanner":
        return Scanner(i=self.i, beacons=self.beacons_absolute + other.beacons_absolute)

    @property
    def beacons_relative(self) -> list[Point]:
        """Provide all beacons in this Scanner, referenced to the Scanner's origin."""
        return self._beacons

    @property
    def beacons_absolute(self) -> list[Point]:
        """Provide all beacons in this Scanner, referenced to a (0, 0, 0) origin."""
        return [beacon + self.origin for beacon in self._beacons]

    def rotate(self, rotation: Rotation) -> "Scanner":
        """Build a new Scanner by applying a Rotation to this Scanner's beacons."""
        rotated_beacons = [b.rotate(rotation=rotation) for b in self.beacons_relative]
        return Scanner(i=self.i, beacons=rotated_beacons)

    @classmethod
    def from_report(cls, report: list[str]) -> "Scanner":
        """Create a new Scanner object by parsing its individual string report."""
        i = int(report[0].removeprefix("--- scanner ").removesuffix(" ---"))
        return cls.from_str(i=i, beacons=report[1:])

    @classmethod
    def from_str(cls, beacons: list[str], i: int = -1) -> "Scanner":
        """Create a new Scanner object by parsing strings representing beacons."""
        beacons = [Point(*map(int, beacon.split(","))) for beacon in beacons]
        return Scanner(i=i, beacons=beacons)


class ScannerAligner:
    """Tool for finding the common rotation and alignment shift between Scanner pairs."""
    def __init__(self, minimum_shared_beacons: int):
        self._min_beacons = minimum_shared_beacons
        self._rotations = list(self.get_cube_rotations())

    @staticmethod
    def get_cube_rotations() -> Iterable[Rotation]:
        """Generate all 24 non-mirroring Rotation transformations of a 3D cube."""
        for x_i, y_i, z_i in permutations((0, 1, 2), r=3):
            for x_sign in [1, -1]:
                for y_sign in [1, -1]:
                    # Build matrix (set z to 1 for now):
                    matrix = numpy.zeros((3, 3), dtype=int)
                    matrix[x_i, 0] = x_sign
                    matrix[y_i, 1] = y_sign
                    matrix[z_i, 2] = 1
                    # Check determinant to avoid rotation + mirror transformations:
                    if numpy.linalg.det(matrix) == -1:
                        matrix[z_i, 2] = -1
                    yield Rotation.from_matrix(matrix)

    def align_to_reference(self, target: Scanner, ref: Scanner) -> None:
        """Try to align a target Scanner with another reference Scanner."""
        distance_array = self._compute_beacon_distances(t=target, r=ref)
        shift = self._find_common_distance(dist_array=distance_array)
        if shift is None:
            raise ValueError("These two Scanner objects can't be aligned.")
        target.origin = ref.origin + shift

    @staticmethod
    def _compute_beacon_distances(t: Scanner, r: Scanner) -> numpy.ndarray:
        """Generate an array of distances between beacons of two Scanner objects."""
        t_beacons, r_beacons = t.beacons_absolute, r.beacons_absolute
        m, n = len(r_beacons), len(t_beacons)
        distances = (r_beacons[i] - t_beacons[j] for i in range(m) for j in range(n))
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

    def align_rotation(self, target: Scanner, ref: Scanner) -> Scanner:
        """Try to align one of the rotations of a Scanner with another reference."""
        for rotation in self._rotations:
            rotated_target = target.rotate(rotation=rotation)
            try:
                self.align_to_reference(target=rotated_target, ref=ref)
            except ValueError:
                continue
            else:
                return rotated_target
        raise ValueError("These two Scanner objects can't be aligned!")


class Constellation:
    """Assortment of all scanners (with their detected beacons) released by the probe."""
    def __init__(self, scanners: list[Scanner]):
        self._scanners = [*scanners]
        self.aligner = ScannerAligner(minimum_shared_beacons=12)
        self.align_scanners()

    @property
    def beacons(self) -> list[Point]:
        """Provide the different beacons detected by this Constellation's scanners."""
        return list(set(chain.from_iterable(s.beacons_absolute for s in self._scanners)))

    @property
    def scanner_distances(self) -> numpy.ndarray:
        """Provide a matrix with relative distances between Scanner pairs."""
        origins = [s.origin for s in self._scanners]
        array = numpy.zeros((len(self._scanners), len(self._scanners)), dtype=int)
        for i in range(len(self._scanners)):
            for j in range(len(self._scanners)):
                array[i, j] = origins[i].distance(other=origins[j])
        return array

    def align_scanners(self):
        """Align all the stored Scanners to a common reference and orientation."""
        unaligned, aligned = [*self._scanners[1:]], [self._scanners[0]]
        ref = self._scanners[0]
        while unaligned:
            target = unaligned.pop(0)
            try:
                aligned_target = self.aligner.align_rotation(target=target, ref=ref)
            except ValueError:
                unaligned.append(target)
            else:
                aligned.append(aligned_target)
                ref += aligned_target
        self._scanners = aligned

    @classmethod
    def from_report(cls, report: list[str]) -> "Constellation":
        """Build a new Constellation from the combination of reports of all scanners."""
        reports = "|".join(report).replace("||", "@").split("@")
        scanners = [Scanner.from_report(report=r.split("|")) for r in reports]
        return Constellation(scanners=scanners)
