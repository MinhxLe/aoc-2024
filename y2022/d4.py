from dataclasses import dataclass
from typing import Tuple

from os_utils import parse_file


@dataclass
class Range:
    start: int
    end: int


def is_within(r1: Range, r2: Range) -> bool:
    return r2.start <= r1.start <= r2.end and r2.start <= r1.end <= r2.end


def overlaps(r1: Range, r2: Range) -> bool:
    return (
        r2.start <= r1.start <= r2.end
        or r2.start <= r1.end <= r2.end
        or r1.start <= r2.start <= r1.end
        or r1.start <= r2.end <= r1.end
    )


def parse_range(s: str) -> Range:
    start_str, end_str = s.split("-", 1)
    return Range(int(start_str), int(end_str))


def parse_line(s: str) -> Tuple[Range, Range]:
    r1_str, r2_str = s.split(",", 1)
    return parse_range(r1_str), parse_range(r2_str)


def p1(range_pairs):
    return len([1 for r1, r2 in range_pairs if is_within(r1, r2) or is_within(r2, r1)])


def p2(range_pairs):
    return len([1 for r1, r2 in range_pairs if overlaps(r1, r2)])


if __name__ == "__main__":
    test_range_pairs = parse_file("y2022/data/d4_small.txt", parse_line)
    range_pairs = parse_file("y2022/data/d4.txt", parse_line)
    p1(range_pairs)
    p2(test_range_pairs)
    p2(range_pairs)
