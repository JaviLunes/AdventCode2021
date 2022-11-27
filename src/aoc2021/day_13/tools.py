# coding=utf-8
"""Tools used for solving the Day 13: Transparent Origami puzzle."""

# Third party imports:
import numpy


class OrigamiInstructions:
    """Instructions for folding the first page of the sub's manual."""
    def __init__(self, recipe: list[str]):
        section_break = [i for i, line in enumerate(recipe) if line == ""][0]
        self.sheet = self._build_sheet(dots=recipe[:section_break])
        self.pending_folds = self._process_folds(folds=recipe[section_break + 1:])
        self.applied_folds = []

    @staticmethod
    def _build_sheet(dots: list[str]) -> numpy.ndarray:
        """Create a blank sheet of sufficient size and fill it with the provided dots."""
        xs = [int(dot.split(",")[0]) for dot in dots]
        ys = [int(dot.split(",")[1]) for dot in dots]
        sheet = numpy.zeros(shape=(max(ys) + 1, max(xs) + 1))
        for i, j in zip(ys, xs):
            sheet[i, j] = 1
        return sheet.astype(bool)

    @staticmethod
    def _process_folds(folds: list[str]):
        """Process each folding instruction included in the input recipe."""
        numpy_axis_map = dict(x=1, y=0)
        folds = [fold.removeprefix("fold along ") for fold in folds]
        axes = [numpy_axis_map[fold.split("=")[0]] for fold in folds]
        lines = [int(fold.split("=")[1]) for fold in folds]
        return list(zip(axes, lines))

    def apply_folds(self, times: int = None):
        """Apply a number of pending folds, or all of them if None is provided."""
        times = len(self.pending_folds) if times is None else times
        for _ in range(times):
            axis, line = self.pending_folds.pop(0)
            self.applied_folds.append([axis, line])
            sheet_1, sheet_2 = self._split_sheet(axis=axis, line=line)
            sheet_2 = numpy.flip(sheet_2, axis=axis)
            self.sheet = numpy.logical_or(sheet_1, sheet_2)

    def _split_sheet(self, axis: int, line: int) -> tuple[numpy.ndarray, numpy.ndarray]:
        """Divide the stored sheet in two along the provided axis and line."""
        if axis:  # X: horizontal split along a vertical line.
            return self.sheet[:, :line], self.sheet[:, line + 1:]
        else:  # Y: vertical split along a horizontal line.
            return self.sheet[:line, :], self.sheet[line + 1:, :]

    @property
    def sheet_code(self) -> str:
        """Code and combine the marked dots in the sheet into an 8-letter string."""
        array = self.sheet.astype(int)
        char_map = {v: k for k, v in DOT_PRINTER_MAP.items()}
        characters = [char_map[tuple(tuple(r) for r in array[:, i:i + 4].tolist())]
                      for i in range(0, 40, 5)]
        return "".join(characters)

    @property
    def visible_dots(self) -> int:
        """Provide the number of visible dots on the sheet."""
        return numpy.sum(self.sheet)


DOT_PRINTER_MAP = dict(
    A=((0, 1, 1, 0), (1, 0, 0, 1), (1, 0, 0, 1), (1, 1, 1, 1), (1, 0, 0, 1),
       (1, 0, 0, 1)),
    B=((1, 1, 1, 0), (1, 0, 0, 1), (1, 1, 1, 0), (1, 0, 0, 1), (1, 0, 0, 1),
       (1, 1, 1, 0)),
    C=((0, 1, 1, 0), (1, 0, 0, 1), (1, 0, 0, 0), (1, 0, 0, 0), (1, 0, 0, 1), 
       (0, 1, 1, 0)),
    D=(),
    E=((1, 1, 1, 1), (1, 0, 0, 0), (1, 1, 1, 0), (1, 0, 0, 0), (1, 0, 0, 0),
       (1, 1, 1, 1)),
    F=((1, 1, 1, 1), (1, 0, 0, 0), (1, 1, 1, 0), (1, 0, 0, 0), (1, 0, 0, 0), 
       (1, 0, 0, 0)),
    G=((0, 1, 1, 0), (1, 0, 0, 1), (1, 0, 0, 0), (1, 0, 1, 1), (1, 0, 0, 1),
       (0, 1, 1, 1)),
    H=(),
    I=(),
    J=((0, 0, 1, 1), (0, 0, 0, 1), (0, 0, 0, 1), (0, 0, 0, 1), (1, 0, 0, 1),
       (0, 1, 1, 0)),
    K=((1, 0, 0, 1), (1, 0, 1, 0), (1, 1, 0, 0), (1, 0, 1, 0), (1, 0, 1, 0), 
       (1, 0, 0, 1)),
    L=((1, 0, 0, 0), (1, 0, 0, 0), (1, 0, 0, 0), (1, 0, 0, 0), (1, 0, 0, 0), 
       (1, 1, 1, 1)),
    M=(),
    N=(),
    O=(),
    P=((1, 1, 1, 0), (1, 0, 0, 1), (1, 0, 0, 1), (1, 1, 1, 0), (1, 0, 0, 0),
       (1, 0, 0, 0)),
    Q=(),
    R=((1, 1, 1, 0), (1, 0, 0, 1), (1, 0, 0, 1), (1, 1, 1, 0), (1, 0, 1, 0),
       (1, 0, 0, 1)),
    S=(),
    T=(),
    U=((1, 0, 0, 1), (1, 0, 0, 1), (1, 0, 0, 1), (1, 0, 0, 1), (1, 0, 0, 1),
       (0, 1, 1, 0)),
    V=(),
    W=(),
    X=(),
    Y=(),
    Z=((1, 1, 1, 1), (0, 0, 0, 1), (0, 0, 1, 0), (0, 1, 0, 0), (1, 0, 0, 0),
       (1, 1, 1, 1)))
