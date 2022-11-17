# coding=utf-8
"""Tools used for solving the Day 3: Binary Diagnostic puzzle."""


class Report:
    """Group of binary values forming the sub's diagnostic report."""
    def __init__(self, *numbers: str):
        self._validate_inputs(*numbers)
        self._numbers = numbers

    @staticmethod
    def _validate_inputs(*numbers):
        """Check that provided inputs are as expected."""
        assert all(n.strip("01") == "" for n in numbers)
        assert len(set(len(n) for n in numbers)) == 1

    @staticmethod
    def _rearrange_by_position(*numbers: str) -> list[list[int]]:
        """Group bits of equal-length binary string numbers by their positions."""
        bit_size = len(numbers[0])
        return [[int(n[b]) for n in numbers] for b in range(bit_size)]

    @staticmethod
    def _count_binary_values(bits: list[int]) -> tuple[int, int]:
        """For a list of binary bits, return the amount of zeros and ones in it."""
        zeros = len([b for b in bits if b == 0])
        ones = len([b for b in bits if b == 1])
        return zeros, ones

    @staticmethod
    def _binary_to_integer(binary: str) -> int:
        """Convert a string of binary bits into its corresponding integer value."""
        return int(f"0b{binary}", 2)

    def _compute_rating(self, oxygen: bool) -> str:
        """Compute the O2/CO2 rating for this Report."""
        keep = self._numbers
        for i in range(len(keep[0])):
            bit_slots = self._rearrange_by_position(*keep)
            target = self._get_bit_criteria(bits=bit_slots[i], oxygen=oxygen)
            keep = [n for n in keep if int(n[i]) == target]
            if len(keep) == 1:
                return keep[0]
        raise RuntimeError("This point should be unreachable!")

    def _get_bit_criteria(self, bits: list[int], oxygen: bool) -> int:
        """Provide the target value determined by the bit criteria."""
        zeros, ones = self._count_binary_values(bits=bits)
        if oxygen:
            return 1 if ones == zeros else (1 if ones > zeros else 0)
        else:
            return 0 if ones == zeros else (0 if ones > zeros else 1)

    @property
    def gamma_rate(self) -> int:
        """Provide the gamma rate value for this Report."""
        bit_slots = self._rearrange_by_position(*self._numbers)
        bits = []
        for slot in bit_slots:
            zeros, ones = self._count_binary_values(bits=slot)
            bits.append(int(ones >= zeros))
        return self._binary_to_integer(binary="".join(str(bit) for bit in bits))

    @property
    def epsilon_rate(self) -> int:
        """Provide the epsilon rate value for this Report."""
        bit_slots = self._rearrange_by_position(*self._numbers)
        bits = []
        for slot in bit_slots:
            zeros, ones = self._count_binary_values(bits=slot)
            bits.append(int(ones < zeros))
        return self._binary_to_integer(binary="".join(str(bit) for bit in bits))

    @property
    def power_consumption(self) -> int:
        """Provide the power consumption value for this Report."""
        return self.gamma_rate * self.epsilon_rate

    @property
    def o2_rating(self) -> int:
        """Provide the O2 generator rating value for this Report."""
        return self._binary_to_integer(binary=self._compute_rating(oxygen=True))

    @property
    def co2_rating(self) -> int:
        """Provide the CO2 scrubber rating value for this Report."""
        return self._binary_to_integer(binary=self._compute_rating(oxygen=False))

    @property
    def life_rating(self) -> int:
        """Provide the life support rating value for this Report."""
        return self.o2_rating * self.co2_rating
