# coding=utf-8
"""Tools used for solving the Day 4: Giant Squid puzzle."""

# Third party imports:
import numpy


class Board:
    """Define a bingo board."""
    def __init__(self, name: str, numbers: list[int]):
        self.name = name
        self._array = numpy.array([*numbers]).reshape(5, 5)

    def mark_draw(self, drawn_number: int):
        """Mark the drawn number in this Board (if present)."""
        self._array = numpy.where(self._array == drawn_number, numpy.nan, self._array)

    @property
    def has_won(self) -> bool:
        """Check whether any row or column of the board is already fully marked."""
        is_nan = numpy.isnan(self._array)
        # noinspection PyUnresolvedReferences
        return numpy.all(a=is_nan, axis=0).any() or numpy.all(a=is_nan, axis=1).any()

    def compute_score(self, drawn_number: int) -> int:
        """Compute the score of this board, given the drawn number."""
        return int(numpy.nansum(self._array)) * drawn_number


class BingoGame:
    """Define a group of Board objects, competing against each other in a bingo game."""
    def play_game(self, boards: list[Board], numbers: list[int]) \
            -> list[tuple[int, str, int]]:
        """Play all rounds, returning the draw, name and score of each winning Board."""
        boards, winners = [*boards], []
        for drawn_number in numbers:
            round_winners = self._play_round(boards=boards, drawn_number=drawn_number)
            if not round_winners:
                continue
            for winner in round_winners:
                boards = [board for board in boards if board.name != winner.name]
                score = winner.compute_score(drawn_number=drawn_number)
                winners.append((drawn_number, winner.name, score))
        return winners

    @staticmethod
    def _play_round(boards: list[Board], drawn_number: int) -> list[Board]:
        """Mark and check all boards, returning all boards that win this round."""
        for board in boards:
            board.mark_draw(drawn_number=drawn_number)
        return [board for board in boards if board.has_won]


def build_boards_from_lines(lines: list[str]) -> list[Board]:
    """Create a list of Board objects from a list of strings representing board lines."""
    lines = [*lines]
    b, boards, board_numbers = 0, [], []
    while lines:
        line = lines.pop(0)
        if not line:
            continue
        board_numbers.extend(list(map(int, line.replace("  ", " ").split())))
        if len(board_numbers) == 25:
            b += 1
            boards.append(Board(name=str(b), numbers=board_numbers))
            board_numbers = []
    return boards
