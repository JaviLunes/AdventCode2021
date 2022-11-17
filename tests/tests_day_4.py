# coding=utf-8
"""Tests for the Day 4: Giant Squid puzzle."""

# Standard library imports:
import unittest

# Local application imports:
from aoc2021.day_4.tools import BingoGame, Board


class FirstExampleTests(unittest.TestCase):
    def setUp(self) -> None:
        """Prepare objects to be tested."""
        self.draws = [7, 4, 9, 5, 11, 17, 23, 2, 0, 14, 21, 24, 10, 16, 13, 6, 15,
                      25, 12, 22, 18, 20, 8, 19, 3, 26, 1]
        board_1 = Board(name="1st", numbers=[
            22, 13, 17, 11, 0, 8, 2, 23, 4, 24, 21, 9, 14, 16, 7, 6, 10, 3, 18, 5, 1,
            12, 20, 15, 19])
        board_2 = Board(name="2nd", numbers=[
            3, 15, 0, 2, 22, 9, 18, 13, 17, 5, 19, 8, 7, 25, 23, 20, 11, 10, 24, 4,
            14, 21, 16, 12, 6])
        board_3 = Board(name="3rd", numbers=[
            14, 21, 17, 24, 4, 10, 16, 15, 9, 19, 18, 8, 23, 26, 20, 22, 11, 13, 6, 5,
            2, 0, 12, 3, 7])
        self.boards = [board_1, board_2, board_3]
        self.game = BingoGame()

    def test_first_winner(self):
        """The first winner is the 3rd board, with a draw of 24 and a score of 4512."""
        winners = self.game.play_game(boards=self.boards, numbers=self.draws)
        draw, name, score = winners[0]
        self.assertEqual(24, draw)
        self.assertEqual("3rd", name)
        self.assertEqual(4512, score)

    def test_last_winner(self):
        """The last winner is the 2nd board, with a draw of 13 and a score of 1924."""
        winners = self.game.play_game(boards=self.boards, numbers=self.draws)
        draw, name, score = winners[-1]
        self.assertEqual(13, draw)
        self.assertEqual("2nd", name)
        self.assertEqual(1924, score)
