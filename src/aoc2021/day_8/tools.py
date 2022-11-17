# coding=utf-8
"""Tools used for solving the Day 8: Seven Segment Search puzzle."""

# Standard library imports:
from itertools import permutations


class Entry:
    """Combination if input signal patterns and output digits for each sub's display."""
    def __init__(self, entry_text: str):
        self._process_entry_text(text=entry_text)
        self._find_wire_map()

    def _process_entry_text(self, text: str):
        """Split, store and validate the components of the provided entry text."""
        pattern_signals, output_signals = text.split("|")
        self._patterns = pattern_signals.strip().split(" ")
        self._outputs = output_signals.strip().split(" ")
        assert len(self._patterns) == 10
        assert len(self._outputs) == 4

    def _find_wire_map(self):
        """Try all possible WireMap objects and register the valid one."""
        wire_maps = build_wire_maps()
        are_valid = {wm: self._try_wire_map(wire_map=wm) for wm in wire_maps}
        valid_wire_maps = [wm for wm, is_valid in are_valid.items() if is_valid]
        assert len(valid_wire_maps) == 1
        self._map = valid_wire_maps[0]

    def _try_wire_map(self, wire_map: "WireMap") -> bool:
        """Attempt to build a valid digit set from stored patterns and input WireMap."""
        digits = set(self._build_digit(
            signals=signals, wire_map=wire_map) for signals in self._patterns)
        return (len(digits) == 10) and ("?" not in digits)

    @staticmethod
    def _build_digit(signals: str, wire_map: "WireMap") -> str:
        """Translate a group of signals and compose a digit with them."""
        return build_digit(signals=wire_map.translate(signals=signals))

    def __repr__(self) -> str:
        return f"{''.join(self.pattern_digits)} | {''.join(self.output_digits)}"

    @property
    def pattern_digits(self) -> tuple[str, ...]:
        """Return the ten digits encoded by this Entry's unique signal patterns."""
        return tuple(self._build_digit(
            signals=signals, wire_map=self._map) for signals in self._patterns)

    @property
    def output_digits(self) -> tuple[str, ...]:
        """Return the four digits encoded by this Entry's digit output value."""
        return tuple(self._build_digit(
            signals=signals, wire_map=self._map) for signals in self._outputs)


class WireMap:
    """Map each of seven possible entry signals to their corresponding output signal."""
    def __init__(self, a: str, b: str, c: str, d: str, e: str, f: str, g: str):
        self._map = dict(a=a, b=b, c=c, d=d, e=e, f=f, g=g)

    def __repr__(self) -> str:
        return "".join(k + v for k, v in self._map.items())

    def translate(self, signals: str) -> str:
        """Translate each signal in the input string using the internal signal map."""
        return "".join(self._map[s] for s in signals)


def build_wire_maps() -> list[WireMap]:
    """Build all possible distinct WireMap objects."""
    return [WireMap(*signals) for signals in permutations("abcdefg")]


def build_digit(signals: str) -> str:
    """Process a string of activation signals to compose a seven-segment 0-9 digit."""
    a = "a" in signals
    b = "b" in signals
    c = "c" in signals
    d = "d" in signals
    e = "e" in signals
    f = "f" in signals
    g = "g" in signals
    digit_options = [
        ("0", (a and b and c and e and f and g) and not d),
        ("1", (c and f) and not (a or b or d or e or g)),
        ("2", (a and c and d and e and g) and not (b or f)),
        ("3", (a and c and d and f and g) and not (b or e)),
        ("4", (b and c and d and f) and not (a or e or g)),
        ("5", (a and b and d and f and g) and not (c or e)),
        ("6", (a and b and d and e and f and g) and not c),
        ("7", (a and c and f) and not (b or d or e or g)),
        ("8", a and b and c and d and e and f and g),
        ("9", (a and b and c and d and f and g) and not e)]
    valid_options = [d[0] for d in digit_options if d[1]]
    return "?" if len(valid_options) != 1 else valid_options[0]
