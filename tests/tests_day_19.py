# coding=utf-8
"""Tests for the Day 19: Beacon Scanner puzzle."""

# Standard library imports:
import unittest

# Local application imports:
from aoc2021.day_19.tools import Scanner, ScannerAligner


class AlignmentTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        self.beacons_0_small = ["0,2,0", "4,1,0", "3,3,0"]
        self.beacons_1_small = ["-1,-1,0", "-5,0,0", "-2,1,0"]
        self.beacons_0_large = [
            "404,-588,-901", "528,-643,409", "-838,591,734", "390,-675,-793",
            "-537,-823,-458", "-485,-357,347", "-345,-311,381", "-661,-816,-575",
            "-876,649,763", "-618,-824,-621", "553,345,-567", "474,580,667",
            "-447,-329,318", "-584,868,-557", "544,-627,-890", "564,392,-477",
            "455,729,728", "-892,524,684", "-689,845,-530", "423,-701,434",
            "7,-33,-71", "630,319,-379", "443,580,662", "-789,900,-551", "459,-707,401"]
        self.beacons_1_large = [
            "686,422,578", "605,423,415", "515,917,-361", "-336,658,858", "95,138,22",
            "-476,619,847", "-340,-569,-846", "567,-361,727", "-460,603,-452",
            "669,-402,600", "729,430,532", "-500,-761,534", "-322,571,750",
            "-466,-666,-811", "-429,-592,574", "-355,545,-477", "703,-491,-529",
            "-328,-685,520", "413,935,-424", "-391,539,-444", "586,-435,557",
            "-364,-763,-893", "807,-499,-711", "755,-354,-619", "553,889,-390"]
        self.beacons_4_large = [
            "727,592,562", "-293,-554,779", "441,611,-461", "-714,465,-776",
            "-743,427,-804", "-660,-479,-426", "832,-632,460", "927,-485,-438",
            "408,393,-506", "466,436,-512", "110,16,151", "-258,-428,682",
            "-393,719,612", "-211,-452,876", "808,-476,-593", "-575,615,604",
            "-485,667,467", "-680,325,-822", "-627,-443,-432", "872,-547,-609",
            "833,512,582", "807,604,487", "839,-516,451", "891,-625,532",
            "-652,-548,-490", "30,-46,-14"]

    def test_align_small_scanners(self):
        """Scanner 1 lays at x5y2z0 offset, no rotation from Scanner 0's frame."""
        s_0 = Scanner.from_str(beacons=self.beacons_0_small)
        s_1 = Scanner.from_str(beacons=self.beacons_1_small)
        self.assertTupleEqual((0, 0, 0), s_1.origin.coordinates)
        aligner = ScannerAligner(minimum_shared_beacons=3)
        aligner.align_to_reference(target=s_1, ref=s_0)
        self.assertTupleEqual((5, 2, 0), s_1.origin.coordinates)

    def test_align_large_scanners_without_rotation(self):
        """Scanner 1 can't be aligned to Scanner 0 without rotating it."""
        s_0 = Scanner.from_str(beacons=self.beacons_0_large)
        s_1 = Scanner.from_str(beacons=self.beacons_1_large)
        aligner = ScannerAligner(minimum_shared_beacons=12)
        with self.assertRaises(ValueError):
            aligner.align_to_reference(target=s_1, ref=s_0)

    def test_align_large_scanners_with_rotation_1(self):
        """One of Scanner 1's rotations can be aligned to Scanner 0."""
        s_0 = Scanner.from_str(beacons=self.beacons_0_large)
        s_1 = Scanner.from_str(beacons=self.beacons_1_large)
        aligner = ScannerAligner(minimum_shared_beacons=12)
        aligner.align_rotation(target=s_1, ref=s_0)

    def test_align_large_scanners_with_rotation_4(self):
        """One of Scanner 4's rotations can be aligned to Scanner 1."""
        s_1 = Scanner.from_str(beacons=self.beacons_1_large)
        s_4 = Scanner.from_str(beacons=self.beacons_4_large)
        aligner = ScannerAligner(minimum_shared_beacons=12)
        aligner.align_rotation(target=s_4, ref=s_1)
