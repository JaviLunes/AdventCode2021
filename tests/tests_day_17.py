# coding=utf-8
"""Tests for the Day 17: Trick Shot puzzle."""

# Standard library imports:
import unittest

# Local application imports:
from aoc2021.day_17.tools import ProbeLauncher


class ExampleTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        self.launcher = ProbeLauncher.from_description(
            target_string="target area: x=20..30, y=-10..-5")

    def test_probe_1_reaches_target_at_given_step(self):
        """The Probe is within the TargetArea only at time step 7."""
        probe = self.launcher.launch(launch_x=7, launch_y=2)
        self.assertTrue(probe.succeeds)
        self.assertEqual(7, probe.t)

    def test_probe_2_reaches_target_at_given_step(self):
        """The Probe is within the TargetArea only at time step 9."""
        probe = self.launcher.launch(launch_x=6, launch_y=3)
        self.assertTrue(probe.succeeds)
        self.assertEqual(9, probe.t)

    def test_probe_3_reaches_target_at_given_step(self):
        """The Probe is within the TargetArea only at time step 4."""
        probe = self.launcher.launch(launch_x=9, launch_y=0)
        self.assertTrue(probe.succeeds)
        self.assertEqual(4, probe.t)

    def test_probe_4_never_reaches_target(self):
        """The Probe is never within the TargetArea."""
        probe = self.launcher.launch(launch_x=17, launch_y=-4)
        self.assertFalse(probe.succeeds)

    def test_find_trick_shot(self):
        """The Probe doing the trick shot reaches a max height of 45."""
        probe = self.launcher.launch_trick_shot(plot=False)
        self.assertEqual(45, probe.max_height)

    def test_find_all_valid_shots(self):
        """There are 112 different ways of launching a Probe and reach the TargetArea."""
        probes = self.launcher.find_valid_shots(plot=False)
        self.assertEqual(112, len(probes))
