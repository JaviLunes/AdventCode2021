# coding=utf-8
"""Tests for the Day 18: Snailfish puzzle."""

# Standard library imports:
import unittest

# Local application imports:
from aoc2021.day_18.tools import Homework, SFNumber


class ExampleNumberTests(unittest.TestCase):
    def test_parsing_structures(self):
        """A string representing a SFNumber can be decomposed into value-depth items."""
        strings = ["[1,2]", "[[1,2],[[3,4],5]]",
                   "[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]"]
        structures = [[(1, 0), (2, 0)], [(1, 1), (2, 1), (3, 2), (4, 2), (5, 1)],
                      [(0, 2), (4, 3), (5, 3), (0, 2), (0, 2),
                       (4, 3), (5, 3), (2, 3), (6, 3), (9, 2), (5, 2)]]
        for string, expected in zip(strings, structures):
            with self.subTest(input=string):
                structure = SFNumber._parse_structure(string=string)
                self.assertListEqual(expected, structure)

    def test_adding_numbers(self):
        """Validate the results of adding two numbers (and reducing the result)."""
        a = SFNumber("[1,2]")
        b = SFNumber("[[3,4],5]")
        c = SFNumber("[[1,2],[[3,4],5]]")
        self.assertEqual(c, a + b)
        a = SFNumber("[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]")
        b = SFNumber("[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]")
        c = SFNumber("[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]")
        self.assertEqual(c, a + b)
        a = SFNumber("[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]")
        b = SFNumber("[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]")
        c = SFNumber("[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]")
        self.assertEqual(c, a + b)
        a = SFNumber("[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]")
        b = SFNumber("[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]")
        c = SFNumber("[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]")
        self.assertEqual(c, a + b)
        a = SFNumber("[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]")
        b = SFNumber("[7,[5,[[3,8],[1,4]]]]")
        c = SFNumber("[[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]")
        self.assertEqual(c, a + b)
        a = SFNumber("[[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]]")
        b = SFNumber("[[2,[2,2]],[8,[8,1]]]")
        c = SFNumber("[[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]")
        self.assertEqual(c, a + b)
        a = SFNumber("[[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]]")
        b = SFNumber("[2,9]")
        c = SFNumber("[[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]")
        self.assertEqual(c, a + b)
        a = SFNumber("[[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]")
        b = SFNumber("[1,[[[9,3],9],[[9,0],[0,7]]]]")
        c = SFNumber("[[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]]")
        self.assertEqual(c, a + b)
        a = SFNumber("[[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]]")
        b = SFNumber("[[[5,[7,4]],7],1]")
        c = SFNumber("[[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]]")
        self.assertEqual(c, a + b)
        a = SFNumber("[[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]]")
        b = SFNumber("[[[[4,2],2],6],[8,7]]")
        c = SFNumber("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]")
        self.assertEqual(c, a + b)

    def test_reducing_numbers(self):
        """Validate the results of (completely) reducing numbers."""
        a = SFNumber(string="[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]")
        b = SFNumber(string="[[[[0,7],4],[[7,8],[6,0]]],[8,1]]")
        a.reduce()
        self.assertEqual(b, a)

    def test_exploding_numbers(self):
        """Validate the results of (completely) exploding numbers."""
        a = SFNumber(string="[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]")
        b = SFNumber(string="[[[[0,7],4],[15,[0,13]]],[1,1]]")
        a.explode()
        self.assertEqual(b, a)
        a = SFNumber(string="[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]")
        b = SFNumber(string="[[[[0,7],4],[[7,8],[6,0]]],[8,1]]")
        a.explode()
        self.assertEqual(b, a)
        a = SFNumber(string="[[[[[9,8],1],2],3],4]")
        b = SFNumber(string="[[[[0,9],2],3],4]")
        a.explode()
        self.assertEqual(b, a)
        a = SFNumber(string="[7,[6,[5,[4,[3,2]]]]]")
        b = SFNumber(string="[7,[6,[5,[7,0]]]]")
        a.explode()
        self.assertEqual(b, a)
        a = SFNumber(string="[[6,[5,[4,[3,2]]]],1]")
        b = SFNumber(string="[[6,[5,[7,0]]],3]")
        a.explode()
        self.assertEqual(b, a)
        a = SFNumber(string="[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]")
        b = SFNumber(string="[[3,[2,[8,0]]],[9,[5,[7,0]]]]")
        a.explode()
        self.assertEqual(b, a)

    def test_splitting_numbers(self):
        """Validate the results of splitting numbers (only once)."""
        a = SFNumber(string="[[[[0,7],4],[15,[0,13]]],[1,1]]")
        b = SFNumber(string="[[[[0,7],4],[[7,8],[0,13]]],[1,1]]")
        a.split()
        self.assertEqual(b, a)
        a = SFNumber(string="[[[[0,7],4],[[7,8],[0,13]]],[1,1]]")
        b = SFNumber(string="[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]")
        a.split()
        self.assertEqual(b, a)

    def test_computer_number_magnitudes(self):
        """Validate the results of compressing a number's structure into a value."""
        a = SFNumber("[9,1]")
        self.assertEqual(29, a.magnitude)
        a = SFNumber("[1,9]")
        self.assertEqual(21, a.magnitude)
        a = SFNumber("[[9,1],[1,9]]")
        self.assertEqual(129, a.magnitude)
        a = SFNumber("[[1,2],[[3,4],5]]")
        self.assertEqual(143, a.magnitude)
        a = SFNumber("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]")
        self.assertEqual(1384, a.magnitude)
        a = SFNumber("[[[[1,1],[2,2]],[3,3]],[4,4]]")
        self.assertEqual(445, a.magnitude)
        a = SFNumber("[[[[3,0],[5,3]],[4,4]],[5,5]]")
        self.assertEqual(791, a.magnitude)
        a = SFNumber("[[[[5,0],[7,4]],[5,5]],[6,6]]")
        self.assertEqual(1137, a.magnitude)
        a = SFNumber("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]")
        self.assertEqual(3488, a.magnitude)
        a = SFNumber("[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]")
        self.assertEqual(4140, a.magnitude)


class ExampleHomeworkTests(unittest.TestCase):
    def test_finding_max_twofold_magnitude(self):
        """Validate the max magnitude achievable by summing two of given numbers."""
        strings = [
            "[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]",
            "[[[5,[2,8]],4],[5,[[9,9],0]]]", "[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]",
            "[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]",
            "[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]",
            "[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]",
            "[[[[5,4],[7,7]],8],[[8,3],8]]", "[[9,3],[[9,9],[6,[4,9]]]]",
            "[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]",
            "[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"]
        homework = Homework(number_strings=strings)
        self.assertEqual(3993, homework.find_max_twofold_magnitude())

    def test_solving_small_homework_1(self):
        """Validate the result of adding multiple numbers together."""
        strings = ["[1,1]", "[2,2]", "[3,3]", "[4,4]"]
        homework = Homework(number_strings=strings)
        expected = SFNumber(string="[[[[1,1],[2,2]],[3,3]],[4,4]]")
        self.assertEqual(expected, homework.sum())

    def test_solving_small_homework_2(self):
        """Validate the result of adding multiple numbers together."""
        strings = ["[1,1]", "[2,2]", "[3,3]", "[4,4]", "[5,5]"]
        homework = Homework(number_strings=strings)
        expected = SFNumber(string="[[[[3,0],[5,3]],[4,4]],[5,5]]")
        self.assertEqual(expected, homework.sum())

    def test_solving_small_homework_3(self):
        """Validate the result of adding multiple numbers together."""
        strings = ["[1,1]", "[2,2]", "[3,3]", "[4,4]", "[5,5]", "[6,6]"]
        homework = Homework(number_strings=strings)
        expected = SFNumber(string="[[[[5,0],[7,4]],[5,5]],[6,6]]")
        self.assertEqual(expected, homework.sum())

    def test_solving_large_homework_1(self):
        """Validate the result of adding multiple numbers together."""
        strings = [
            "[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]",
            "[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]",
            "[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]",
            "[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]",
            "[7,[5,[[3,8],[1,4]]]]", "[[2,[2,2]],[8,[8,1]]]", "[2,9]",
            "[1,[[[9,3],9],[[9,0],[0,7]]]]", "[[[5,[7,4]],7],1]",
            "[[[[4,2],2],6],[8,7]]"]
        homework = Homework(number_strings=strings)
        expected = SFNumber(
            string="[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]")
        self.assertEqual(expected, homework.sum())

    def test_solving_large_homework_2(self):
        """Validate the result of adding multiple numbers together."""
        strings = [
            "[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]",
            "[[[5,[2,8]],4],[5,[[9,9],0]]]",
            "[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]",
            "[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]",
            "[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]",
            "[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]",
            "[[[[5,4],[7,7]],8],[[8,3],8]]",
            "[[9,3],[[9,9],[6,[4,9]]]]",
            "[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]",
            "[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"]
        homework = Homework(number_strings=strings)
        expected = SFNumber(
            string="[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]")
        self.assertEqual(expected, homework.sum())
