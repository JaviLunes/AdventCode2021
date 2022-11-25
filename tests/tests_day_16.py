# coding=utf-8
"""Tests for the Day 16: Packet Decoder puzzle."""

# Standard library imports:
import unittest

# Local application imports:
from aoc2021.day_16.tools import Packet, OperatorPacket, ValuePacket


class ExampleTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        self.hex_v = "D2FE28"
        self.hex_o1 = "38006F45291200"
        self.hex_o2 = "EE00D40C823060"
        self.bin_v = "110100101111111000101000"
        self.bin_o1 = "00111000000000000110111101000101001010010001001000000000"
        self.bin_o2 = "11101110000000001101010000001100100000100011000001100000"

    def test_building_operator_packet_1(self):
        """The specifications of the built Packet must match the expected values."""
        packet = Packet.from_binary(bin_string=self.bin_o1)
        self.assertIsInstance(packet, OperatorPacket)
        self.assertEqual(1, packet.version)
        self.assertEqual(2, len(packet.data))
        self.assertEqual(49, packet.bits)

    def test_building_operator_packet_2(self):
        """The specifications of the built Packet must match the expected values."""
        packet = Packet.from_binary(bin_string=self.bin_o2)
        self.assertIsInstance(packet, OperatorPacket)
        self.assertEqual(7, packet.version)
        self.assertEqual(3, len(packet.data))
        self.assertEqual(51, packet.bits)

    def test_building_value_packet(self):
        """The specifications of the built Packet must match the expected values."""
        packet = Packet.from_binary(bin_string=self.bin_v)
        self.assertIsInstance(packet, ValuePacket)
        self.assertEqual(6, packet.version)
        self.assertEqual(2021, packet.data)

    def test_compute_sum_of_versions(self):
        """Sum the version of a Packet with the total version of all its sub Packets."""
        packet = Packet.from_hexadecimal(hex_string="8A004A801A8002F478")
        self.assertEqual(16, packet.total_version)
        packet = Packet.from_hexadecimal(hex_string="620080001611562C8802118E34")
        self.assertEqual(12, packet.total_version)
        packet = Packet.from_hexadecimal(hex_string="C0015000016115A2E0802F182340")
        self.assertEqual(23, packet.total_version)
        packet = Packet.from_hexadecimal(hex_string="A0016C880162017C3686B18A3D4780")
        self.assertEqual(31, packet.total_version)

    def test_compute_transmission_value(self):
        """Sum the value of a Packet with the value of all its sub Packets."""
        packet = Packet.from_hexadecimal(hex_string="C200B40A82")
        self.assertEqual(3, packet.value)
        packet = Packet.from_hexadecimal(hex_string="04005AC33890")
        self.assertEqual(54, packet.value)
        packet = Packet.from_hexadecimal(hex_string="880086C3E88112")
        self.assertEqual(7, packet.value)
        packet = Packet.from_hexadecimal(hex_string="CE00C43D881120")
        self.assertEqual(9, packet.value)
        packet = Packet.from_hexadecimal(hex_string="D8005AC2A8F0")
        self.assertEqual(1, packet.value)
        packet = Packet.from_hexadecimal(hex_string="F600BC2D8F")
        self.assertEqual(0, packet.value)
        packet = Packet.from_hexadecimal(hex_string="9C005AC2F8F0")
        self.assertEqual(0, packet.value)
        packet = Packet.from_hexadecimal(hex_string="9C0141080250320F1802104A08")
        self.assertEqual(1, packet.value)

    def test_hexadecimal_to_binary(self):
        """Match the hexadecimal strings to their corresponding binary strings."""
        self.assertEqual(self.bin_v, Packet._hex_to_bin(string=self.hex_v))
        self.assertEqual(self.bin_o1, Packet._hex_to_bin(string=self.hex_o1))
        self.assertEqual(self.bin_o2, Packet._hex_to_bin(string=self.hex_o2))
