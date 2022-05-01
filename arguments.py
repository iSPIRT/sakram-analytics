#!/usr/bin/env python3
"""
Parse command line arguments.

Author: Dhruva Kashyap
"""

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    """Parse CLI args."""
    parser = argparse.ArgumentParser(description="pesu_security")
    parser.add_argument(
        "--name",
        type=str,
        default="test_temp",
        help="Name of experiment",
    )
    parser.add_argument(
        "--logging",
        default="DEBUG",
    )
    return parser.parse_args()


def show_args(args: argparse.Namespace) -> None:
    """Print args."""
    NUM: int = 40
    max_len: int = 10
    print("=" * NUM)
    for i in vars(args):
        ai = getattr(args, i)
        print(
            f"{i}{' '*(max_len-len(i))}[{type(ai).__name__}]"
            + f"{' '*(max_len-len(type(ai).__name__))}------> {ai}"
        )
    print("=" * NUM)


if __name__ == "__main__":
    show_args(parse_args())
