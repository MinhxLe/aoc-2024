from dataclasses import dataclass
from typing import Literal, Tuple
import numpy as np

MAX_HEIGHT = 5


@dataclass
class Schematic:
    type_: Literal["key", "lock"]
    heights: list[int]

    def __post_init__(self):
        assert len(self.heights) == 5
        assert all(0 <= h <= MAX_HEIGHT for h in self.heights)


@dataclass
class Key:
    heights: list[int]

    def __post_init__(self):
        assert len(self.heights) == 5
        assert all(0 <= h <= MAX_HEIGHT for h in self.heights)


def parse_grid(s: str) -> np.ndarray:
    rows = [r for r in s.split("\n") if r]
    return np.array([[c == "#" for c in list(row)] for row in rows])


def parse_file(fname) -> list[Schematic]:
    schematics = []
    with open(fname) as f:
        content = f.read()
    grid_strs = content.split("\n\n")
    for grid_str in grid_strs:
        grid = parse_grid(grid_str)
        # since 1 of the rows must does not contribute to the height
        heights = np.sum(grid, axis=0) - 1
        if np.all(grid[0, :]):
            type_ = "lock"
        elif np.all(grid[-1, :]):
            type_ = "key"
        else:
            raise ValueError
        schematics.append(Schematic(type_, list(heights)))

    return schematics


def is_compatible(s1: Schematic, s2: Schematic) -> bool:
    is_different_type = (s1.type_ == "key" and s2.type_ == "lock") or (
        s1.type_ == "lock" and s2.type_ == "key"
    )
    has_compatible_heights = all(
        kh + lh <= MAX_HEIGHT for kh, lh in zip(s1.heights, s2.heights)
    )
    return is_different_type and has_compatible_heights


def part1(fname):
    schematics = parse_file(fname)
    keys = [s for s in schematics if s.type_ == "key"]
    locks = [s for s in schematics if s.type_ == "lock"]
    total = 0
    for key in keys:
        for lock in locks:
            if is_compatible(key, lock):
                print(key, lock)
                total += 1
    return total


if __name__ == "__main__":
    test_fname = "y2024/data/d25_small.txt"
    fname = "y2024/data/d25.txt"
    part1(fname)
