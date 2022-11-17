# coding=utf-8
"""Compute the solution of the Day 4: Giant Squid puzzle."""

# Local application imports:
from aoc2021.common import read_puzzle_input
from aoc2021.day_4.tools import BingoGame, build_boards_from_lines

print("\nDay 4: Giant Squid.")
# Part one:
lines = read_puzzle_input(day=4)
draw_numbers = list(map(int, lines[0].split(",")))
boards = build_boards_from_lines(lines=lines[2:])
game = BingoGame()
winners = game.play_game(boards=boards, numbers=draw_numbers)
print(f"    The solution to part one is: {winners[0][2]}")

# Part two:
print(f"    The solution to part two is: {winners[-1][2]}")
