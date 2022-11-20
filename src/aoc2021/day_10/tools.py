# coding=utf-8
"""Tools used for solving the Day 10: Syntax Scoring puzzle."""

# Standard library imports:
from statistics import median


class NavigationLine:
    """Individual line of code in the navigation subsystem."""
    def __init__(self, chars: str):
        self.chars = chars

    def _analyze_chunks(self) -> tuple[str, int]:
        """Parse this line, returning the corruption or non-closed chars, and flag."""
        openings = ("(", "[", "{", "<")
        active_chunks = []
        for char in self.chars:
            if char in openings:
                active_chunks.append(char)  # New, still open chunk.
            elif self._get_opening(char=char) == active_chunks[-1]:
                active_chunks.pop(-1)  # Valid char closing the last open chunk.
            else:  # Invalid closing char.
                return char, 1
        if active_chunks:
            return "".join(active_chunks), 2  # Non-closed chunks.
        return "", 0  # Nothing to report.

    @staticmethod
    def _get_opening(char: str) -> str:
        """Translate a closing character into its corresponding opening character."""
        char_map = {")": "(", "]": "[", "}": "{", ">": "<"}
        return char_map[char]

    @property
    def corruption_score(self) -> int:
        """Provide the corruption score for this NavigationLine (if appropriate)."""
        char_map = {")": 3, "]": 57, "}": 1197, ">": 25137}
        output, flag = self._analyze_chunks()
        return 0 if flag != 1 else char_map[output]

    @property
    def completion_score(self) -> int:
        """Provide the completion score for this NavigationLine (if appropriate)."""
        char_map = {"(": 1, "[": 2, "{": 3, "<": 4}
        output, flag = self._analyze_chunks()
        if flag != 2:
            return 0
        score = 0
        for char in reversed(output):
            score = score * 5 + char_map[char]
        return score


class SyntaxChecker:
    """Tool for identifying corrupt or incomplete lines in a navigation subsystem."""
    def __init__(self, lines: list[str]):
        self.lines = [NavigationLine(chars=line) for line in lines]

    @property
    def corruption_score(self) -> int:
        """Provide the sum of scores for corrupt lines."""
        return sum(line.corruption_score for line in self.lines)

    @property
    def completion_score(self) -> int:
        """Provide the sum of scores for uncompleted lines."""
        scores = [line.completion_score for line in self.lines]
        return median(filter(lambda c: c > 0, scores))
