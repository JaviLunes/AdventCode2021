# coding=utf-8
"""Tests for the Day 2: Dive! puzzle."""

# Standard library imports:
import unittest

# Local application imports:
from aoc2021.day_2.tools import Submarine, AimSubmarine


class ExampleTests(unittest.TestCase):
    def setUp(self) -> None:
        """Prepare objects to be tested."""
        course = [("forward", 5), ("down", 5), ("forward", 8), ("up", 3), ("down", 8),
                  ("forward", 2)]
        self.submarine = Submarine()
        self.submarine.implement_course(course=course)
        self.aim_submarine = AimSubmarine()
        self.aim_submarine.implement_course(course=course)

    def test_location_after_course(self):
        """The course represents a horizontal and diving movements of 15 and 10."""
        self.assertEqual(15, self.submarine.horizontal)
        self.assertEqual(10, self.submarine.depth)
        self.assertEqual(150, self.submarine.total_movement)

    def test_location_after_course_using_aim(self):
        """The course represents a horizontal and diving movements of 15 and 60."""
        self.assertEqual(15, self.aim_submarine.horizontal)
        self.assertEqual(60, self.aim_submarine.depth)
        self.assertEqual(900, self.aim_submarine.total_movement)
