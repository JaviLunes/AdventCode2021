# coding=utf-8
"""Main access point for command-line execution of core functions."""

# Standard library imports:
import sys

# Local application imports:
from aoc2021.common import build_all_templates, build_templates
from aoc2021.common import compute_all_solutions, compute_solution


def main():
    """Main function managing execution requests of core functions from command line."""
    try:
        _, flag, *args = sys.argv
        assert flag in ["-h", "--help", "-b", "--build", "-s", "--solve"]
        day = -1 if not args else int(args[0])
    except (ValueError, AssertionError):
        print("Value Error: Provided command line arguments are not valid.")
        _print_help()
        sys.exit(2)
    else:
        if flag in ("-h", "--help"):
            _print_help()
            sys.exit(0)
        elif flag in ("-b", "--build"):
            if day == -1:
                build_all_templates()
            else:
                build_templates(day=day)
        elif flag in ("-s", "--solve"):
            if day == -1:
                compute_all_solutions()
            else:
                compute_solution(day=day)
        else:
            print(f"Value Error: Unrecognised '{flag}' flag.")
            _print_help()
            sys.exit(2)


def _print_help():
    """Print usage information about the main function and its parameters."""
    usage = f"""\nUsage:
        -m aoc2021 [OPTION] [day]
    Arguments:
        -h, --help:
            Display this usage message and exit.
        -b, --build:
            Generate template files for solving and testing the provided day.
        -s, --solve:
            Compute and print the solutions to the puzzle of the provided day.
        day:
            Puzzle number to build/solve. If -1 or not provided and building, 
            all not yet built puzzles will be built. If -1 or not provided 
            and solving, all built puzzles will be solved.
    """.replace("\n    ", "\n")
    print(usage)


# Execute main code:
if __name__ == "__main__":
    main()
