# coding=utf-8
"""Tools used for solving the Day 14: Extended Polymerization puzzle."""

# Standard library imports:
from collections import Counter


class Polymer:
    """Template and rules for evolving a polymer material able to reinforce the sub."""
    def __init__(self, recipe: list[str]):
        pairs = [a + b for a, b in zip(recipe[0][:-1], recipe[0][1:])]
        self.pairs_counter = Counter(pairs)
        self.elements_counter = Counter(recipe[0])
        self.rules = self._process_rules(rules=recipe[2:])

    @staticmethod
    def _process_rules(rules: list[str]) -> dict[str, str]:
        """Process each provided pair insertion rule."""
        pairs = [rule.split(" -> ")[0] for rule in rules]
        inserts = [rule.split(" -> ")[1] for rule in rules]
        return {p: i for p, i in zip(pairs, inserts)}

    def polymerize_for(self, times: int):
        """Apply all compatible insertion rules to this Polymer for a number of times."""
        [self._polymerize() for _ in range(times)]

    def _polymerize(self):
        """Apply all compatible insertion rules to the stored polymer, and update it."""
        counter = Counter()
        for (e1, e2), amount in self.pairs_counter.items():
            insert = self.rules.get(e1 + e2, "")
            counter.update({e1 + insert: amount, insert + e2: amount})
            self.elements_counter.update({insert: amount})
        self.pairs_counter = counter

    @property
    def element_freq_delta(self) -> int:
        """Compute the frequency delta between the most and least common elements."""
        return max(self.elements_counter.values()) - min(self.elements_counter.values())

    @property
    def length(self) -> int:
        """Provide the length of the sequence of elements conforming this Polymer."""
        return self.pairs_counter.total() + 1
