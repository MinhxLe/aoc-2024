from dataclasses import dataclass
from typing import Tuple
from grid import V2, Grid, is_inbounds, read_grid
import string


def get_part_number_range(grid: Grid, p: V2) -> Tuple[int, int]:
    assert grid.at(p) in string.digits
    row = grid[p.x]
    start_idx, end_idx = p.y, p.y + 1
    # start idx is inclusive so we need to look ahead
    while start_idx - 1 >= 0 and row[start_idx - 1] in string.digits:
        start_idx -= 1
    while end_idx < len(row) and row[end_idx] in string.digits:
        end_idx += 1
    return start_idx, end_idx


def is_adjacent(grid: Grid, p: V2, s: str) -> bool:
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            else:
                new_p = p + V2(dx, dy)
                if grid.is_inbounds(new_p) and grid.at(new_p) == s:
                    return True
    return False


def get_adjacent_symbols(grid: Grid, p: V2) -> list[str]:
    symbols = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            else:
                new_p = p + V2(dx, dy)
                if grid.is_inbounds(new_p):
                    symbols.append(grid.at(new_p))
    return symbols


def get_part_numbers(grid: Grid):
    visited = set()
    numbers = []
    for x in range(grid.height):
        for y in range(grid.width):
            p = V2(x, y)
            if p not in visited and grid.at(p) in string.digits:
                start_y, end_y = get_part_number_range(grid, p)
                is_adjacent_to_symbol = False
                for y_prime in range(start_y, end_y):
                    if any(
                        [
                            s != "." and s not in string.digits
                            for s in get_adjacent_symbols(grid, V2(x, y_prime))
                        ]
                    ):
                        is_adjacent_to_symbol = True
                        break
                if is_adjacent_to_symbol:
                    visited |= {V2(x, y_prime) for y_prime in range(start_y, end_y)}
                    numbers.append(int(grid[x][start_y:end_y]))

    return numbers


@dataclass
class Gear:
    n1: int
    n2: int


def maybe_get_gear(grid: Grid, p: V2) -> Gear | None:
    if grid.at(p) != "*":
        return None
    visited = set()
    nums = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            else:
                adj_p = p + V2(dx, dy)
                if (
                    adj_p not in visited
                    and grid.is_inbounds(adj_p)
                    and grid.at(adj_p) in string.digits
                ):
                    start_y, end_y = get_part_number_range(grid, adj_p)
                    nums.append(int(grid[adj_p.x][start_y:end_y]))
                    visited |= {
                        V2(adj_p.x, y_prime) for y_prime in range(start_y, end_y)
                    }
    if len(nums) != 2:
        return None
    else:
        return Gear(nums[0], nums[1])


def get_gears(grid: Grid) -> list[Gear]:
    gears = []
    for x in range(grid.height):
        for y in range(grid.width):
            p = V2(x, y)
            gear = maybe_get_gear(grid, p)
            if gear is not None:
                gears.append(gear)
    return gears


def p1(fname):
    grid = read_grid(fname)
    numbers = get_part_numbers(grid)
    print(sum(numbers))


def p2(fname):
    grid = read_grid(fname)
    gears = get_gears(grid)
    total = sum([g.n1 * g.n2 for g in gears])
    print(total)


def test_get_part_numbers():
    grid = Grid(
        [
            "467..114..",
            "...*......",
            "..35..633.",
            "......#...",
            "617*......",
            ".....+.58.",
            "..592.....",
            "......755.",
            "...$.*....",
            ".664.598..",
        ]
    )
    numbers = get_part_numbers(grid)


def test_get_gears():
    grid = Grid(
        [
            "467..114..",
            "...*......",
            "..35..633.",
            "......#...",
            "617*......",
            ".....+.58.",
            "..592.....",
            "......755.",
            "...$.*....",
            ".664.598..",
        ]
    )
    gears = get_gears(grid)
