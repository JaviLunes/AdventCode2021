# coding=utf-8
"""Tests for the Day 12: Passage Pathing puzzle."""

# Standard library imports:
import unittest

# Local application imports:
from aoc2021.day_12.tools import CaveSystem


class ExampleTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        self.small_system = CaveSystem.from_paths(paths=[
            "start-A", "start-b", "A-c", "A-b", "b-d", "A-end", "b-end"])
        self.medium_system = CaveSystem.from_paths(paths=[
            "dc-end", "HN-start", "start-kj", "dc-start", "dc-HN", "LN-dc", "HN-end",
            "kj-sa", "kj-HN", "kj-dc"])
        self.large_system = CaveSystem.from_paths(paths=[
            "fs-end", "he-DX", "fs-he", "start-DX", "pj-DX", "end-zg", "zg-sl",
            "zg-pj", "pj-he", "RW-he", "fs-DX", "pj-RW", "zg-RW", "start-pj", "he-WI",
            "zg-he", "pj-fs", "start-RW"])

    def test_paths_in_small_cave_system(self):
        """The number of valid paths is 10."""
        self.assertEqual(10, len(self.small_system.compute_valid_paths()))

    def test_paths_in_medium_cave_system(self):
        """The number of valid paths is 19."""
        self.assertEqual(19, len(self.medium_system.compute_valid_paths()))

    def test_paths_in_large_cave_system(self):
        """The number of valid paths is 226."""
        self.assertEqual(226, len(self.large_system.compute_valid_paths()))

    def test_relaxed_paths_in_small_cave_system(self):
        """The number of valid paths is 36."""
        self.assertEqual(36, len(self.small_system.compute_relaxed_paths()))

    def test_relaxed_paths_in_medium_cave_system(self):
        """The number of valid paths is 103."""
        self.assertEqual(103, len(self.medium_system.compute_relaxed_paths()))

    def test_relaxed_paths_in_large_cave_system(self):
        """The number of valid paths is 3509."""
        self.assertEqual(3509, len(self.large_system.compute_relaxed_paths()))
