# coding=utf-8
"""Tools used for solving the Day 16: Packet Decoder puzzle."""

# Standard library imports:
import abc
import math
import re
from typing import Any, Iterable


class Packet(metaclass=abc.ABCMeta):
    """Numeric expression encoded using the Buoyancy Interchange Transmission System."""
    _rx_headers = r"(?P<version>[0,1]{3})(?P<type_id>[0,1]{3})"
    _rx_data = ""

    def __init__(self, version: int, type_id: int, data, bits: int):
        self.version = version
        self.type_id = type_id
        self.data = data
        self.bits = bits

    @classmethod
    def from_hexadecimal(cls, hex_string: str) -> "Packet":
        """Build a Packet-derived object from a hexadecimal string."""
        return cls.from_binary(bin_string=cls._hex_to_bin(string=hex_string))

    @staticmethod
    def _hex_to_bin(string: str) -> str:
        """Transform a hexadecimal string into a binary string."""
        hex_to_bin = {
            "0": "0000", "1": "0001", "2": "0010", "3": "0011", "4": "0100",
            "5": "0101", "6": "0110", "7": "0111", "8": "1000", "9": "1001",
            "A": "1010", "B": "1011", "C": "1100", "D": "1101", "E": "1110", "F": "1111"}
        return "".join(hex_to_bin[char] for char in string)

    @classmethod
    def from_binary(cls, bin_string: str) -> "Packet":
        """Build a Packet-derived object from a binary string."""
        match = re.match(pattern=cls._rx_headers, string=bin_string)
        version = int(match["version"], 2)
        type_id = int(match["type_id"], 2)
        sub_cls = ValuePacket if type_id == 4 else OperatorPacket
        data, bits = sub_cls.extract_data(bin_string=bin_string)
        return sub_cls(version=version, type_id=type_id, data=data, bits=bits)

    @classmethod
    @abc.abstractmethod
    def extract_data(cls, bin_string: str) -> tuple[Any, int]:
        """Extract the internal data and compute the total number of used bits."""
        raise NotImplementedError

    @staticmethod
    def matched_bits(match: re.Match) -> int:
        """Compute the bit length of the matched substring."""
        return match.span()[1] - match.span()[0]

    @property
    @abc.abstractmethod
    def value(self) -> int:
        """Provide the value of this Packet."""
        raise NotImplementedError

    @property
    def total_version(self) -> int:
        """Provide the combination of the own version and versions of all sub packets."""
        return self.version


class ValuePacket(Packet):
    """Packet class encoding an integer value."""
    _rx_data = r"(?P<value>(1[0,1]{4})*0[0,1]{4})"

    @classmethod
    def extract_data(cls, bin_string: str) -> tuple[int, int]:
        """Extract the integer value and compute the total number of used bits."""
        match = re.match(pattern=cls._rx_headers + cls._rx_data, string=bin_string)
        value = int("".join(cls.decode_data(string=match["value"])), 2)
        bits = cls.matched_bits(match=match)
        return value, bits

    @staticmethod
    def decode_data(string: str) -> Iterable[str]:
        """Divide a binary data string into 4-bit groups, removing bit prefixes."""
        for i in range(0, len(string), 5):
            yield string[i:i + 5][-4:]

    @property
    def value(self) -> int:
        """Provide the value of this Packet."""
        return self.data


class OperatorPacket(Packet):
    """Packet class encoding an operation applied over one or more Packet objects."""
    _rx_data = r"((0(?P<length>[0,1]{15}))|(1(?P<number>[0,1]{11})))"

    @classmethod
    def extract_data(cls, bin_string: str) -> tuple[list[Packet], int]:
        """Extract the list of sub-packets and compute the total number of used bits."""
        match = re.match(pattern=cls._rx_headers + cls._rx_data, string=bin_string)
        main_bits = match.span()[1] - match.span()[0]
        remains = bin_string[main_bits:]
        if match["length"] is not None:
            remains = remains[:int(match["length"], 2)]
            sub_packets = cls._get_sub_packets(bin_string=remains, n=None)
        elif match["number"] is not None:
            n = int(match["number"], 2)
            sub_packets = cls._get_sub_packets(bin_string=remains, n=n)
        else:
            raise ValueError
        bits = main_bits + sum(sub.bits for sub in sub_packets)
        return sub_packets, bits

    @staticmethod
    def _get_sub_packets(bin_string: str, n: int = None) -> list["Packet"]:
        """Extract the first 'n' Packets from a binary string, or all if 'n' is None."""
        sub_packets = []
        n = n if n is not None else len(bin_string)
        while "1" in bin_string:
            n -= 1
            packet = ValuePacket.from_binary(bin_string=bin_string)
            bin_string = bin_string[packet.bits:]
            sub_packets.append(packet)
            if n == 0:
                break
        return sub_packets

    @property
    def value(self) -> int:
        """Provide the value of this Packet."""
        if self.type_id == 0:
            return sum(sub.value for sub in self.data)
        elif self.type_id == 1:
            return math.prod(sub.value for sub in self.data)
        elif self.type_id == 2:
            return min(sub.value for sub in self.data)
        elif self.type_id == 3:
            return max(sub.value for sub in self.data)
        elif self.type_id == 5:
            return int(self.data[0].value > self.data[1].value)
        elif self.type_id == 6:
            return int(self.data[0].value < self.data[1].value)
        elif self.type_id == 7:
            return int(self.data[0].value == self.data[1].value)
        else:
            raise KeyError

    @property
    def total_version(self) -> int:
        """Provide the combination of the own version and versions of all sub packets."""
        return self.version + sum(sub.total_version for sub in self.data)
