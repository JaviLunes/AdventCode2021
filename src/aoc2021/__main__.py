# coding=utf-8
"""Main access point for command-line execution of core functions."""

# Standard library imports:
import sys

# Local application imports:
from aoc2021.common import compute_all_solutions, compute_solution


def main():
    """Main function managing execution requests of core functions from command line."""
    try:
        _, *args = sys.argv
        day = -1 if not args else args[0]
    except ValueError:
        print("Value Error: Provided command line arguments are not valid.")
        _print_help()
        sys.exit(2)
    else:
        if day == -1:
            compute_all_solutions()
        else:
            compute_solution(day=int(day))


def _print_help():
    """Print usage information about the main function and its parameters."""
    usage = f"""\nUsage:
        -m aoc2021 [day]
    Arguments:
        day:    Puzzle number to solve. If -1 or not provided, all 
                available puzzles will be solved.
    """.replace("\n    ", "\n")
    print(usage)


# Execute main code:
if __name__ == "__main__":
    main()
