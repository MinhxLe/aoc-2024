from os import WCOREDUMP
from typing import List
from dataclasses import dataclass
import itertools


Grid = List[str]


@dataclass
class V2:
    x: int
    y: int

    def __add__(self, that: "V2") -> "V2":
        return V2(self.x + that.x, self.y + that.y)


def is_char(grid: Grid, position: V2, c: str) -> bool:
    return (
        0 <= position.x < len(grid)
        and 0 <= position.y < len(grid[0])
        and grid[position.x][position.y] == c
    )


def is_word(
    word: str,
    grid: Grid,
    position: V2,
    direction: V2,
) -> bool:
    is_word = True
    for c in word:
        if is_char(grid, position, c):
            position += direction
        else:
            is_word = False
            break
    return is_word


def is_x_mas(grid: Grid, pos: V2) -> bool:
    ul = pos + V2(-1, -1)
    bl = pos + V2(-1, 1)
    ur = pos + V2(1, -1)
    br = pos + V2(1, 1)
    return (
        is_char(grid, pos, "A")
        and (
            (is_char(grid, ul, "M") and is_char(grid, br, "S"))
            or (is_char(grid, ul, "S") and is_char(grid, br, "M"))
        )
        and (
            (is_char(grid, bl, "M") and is_char(grid, ur, "S"))
            or (is_char(grid, bl, "S") and is_char(grid, ur, "M"))
        )
    )


def find_word_count(
    word: str,
    grid: Grid,
) -> int:
    assert len(grid) > 0
    assert len(grid[0]) > 0
    count = 0
    for x, y in itertools.product(range(len(grid)), range(len(grid[0]))):
        for dx, dy in itertools.product([-1, 0, 1], [-1, 0, 1]):
            if not (dx == 0 and dy == 0):
                count += 1 if is_word(word, grid, V2(x, y), V2(dx, dy)) else 0
    return count


def find_xmas_count(grid: Grid):
    assert len(grid) > 0
    assert len(grid[0]) > 0
    count = 0
    for x, y in itertools.product(range(len(grid)), range(len(grid[0]))):
        if is_x_mas(grid, V2(x, y)):
            count += 1
    return count


grid = []
with open("data/day4.txt") as f:
    grid = [line.strip() for line in f]

find_word_count("XMAS", grid)
print(find_xmas_count(grid))
