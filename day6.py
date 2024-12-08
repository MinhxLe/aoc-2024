from enum import StrEnum
from typing import List, Literal, Tuple
from dataclasses import dataclass


class Direction(StrEnum):
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"

    @classmethod
    def all(cls):
        return [x for x in cls]


@dataclass(frozen=True)
class V2:
    x: int
    y: int

    def __add__(self, that: "V2") -> "V2":
        return V2(self.x + that.x, self.y + that.y)


def rotate(direction: Direction) -> Direction:
    match direction:
        case Direction.UP:
            return Direction.RIGHT
        case Direction.DOWN:
            return Direction.LEFT
        case Direction.LEFT:
            return Direction.UP
        case Direction.RIGHT:
            return Direction.DOWN
        case _:
            raise ValueError


Grid = List[str]


def in_bounds(position: V2, grid: Grid) -> bool:
    return 0 <= position.x < len(grid) and 0 <= position.y < len(grid[1])


def is_valid_position(position: V2, grid: Grid) -> bool:
    return in_bounds(position, grid) and grid[position.x][position.y] != "#"


def find_guard(grid: Grid) -> Tuple[Direction, V2]:
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] in Direction.all():
                return Direction(grid[i][j]), V2(i, j)
    raise ValueError("Not found")


def traverse(
    direction: Direction,
    position: V2,
    grid: Grid,
) -> Tuple[list[V2], bool]:
    dp = {
        Direction.DOWN: V2(1, 0),
        Direction.UP: V2(-1, 0),
        Direction.LEFT: V2(0, -1),
        Direction.RIGHT: V2(0, 1),
    }[direction]
    visited_positions = []
    while is_valid_position(position, grid):
        visited_positions.append(position)
        position += dp

    return visited_positions, in_bounds(position, grid)


def count_visited_positions(grid: Grid) -> int:
    direction, position = find_guard(grid)
    visited = set()
    is_inbound = True
    while (direction, position) not in visited and is_inbound:
        visited_positions, is_inbound = traverse(direction, position, grid)
        for visited_position in visited_positions:
            visited.add((direction, visited_position))
        position = visited_positions[-1]
        direction = rotate(direction)
    return len({x[1] for x in visited})


def is_valid_loop(grid: Grid) -> bool:
    direction, position = find_guard(grid)
    visited = set()
    is_inbound = True
    while (direction, position) not in visited and is_inbound:
        visited_positions, is_inbound = traverse(direction, position, grid)
        for visited_position in visited_positions:
            visited.add((direction, visited_position))
        position = visited_positions[-1]
        direction = rotate(direction)
    return is_inbound


def replace_char(s: str, idx: int, c: str) -> str:
    return s[:idx] + c + s[idx + 1 :]


def count_potential_loops(grid: Grid) -> int:
    count = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            print(i, j)
            if grid[i][j] == ".":
                grid[i] = replace_char(grid[i], j, "#")
                if is_valid_loop(grid):
                    count += 1
                grid[i] = replace_char(grid[i], j, ".")
    return count


with open("data/day6.txt") as f:
    grid = [r.strip() for r in f]
test_grid = [
    "....#.....",
    ".........#",
    "..........",
    "..#.......",
    ".......#..",
    "..........",
    ".#..^.....",
    "........#.",
    "#.........",
    "......#...",
]
assert count_visited_positions(test_grid) == 41
assert count_visited_positions(grid) == 5131


print(count_potential_loops(test_grid))
print(count_potential_loops(grid))
