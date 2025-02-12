from dataclasses import dataclass
from typing import Literal
import numpy as np
import copy

EMPTY_BRICK_ID = -1


@dataclass
class Coord:
    x: int
    y: int
    z: int

    def __lt__(self, that):
        return self.x < that.x or self.y < that.y or self.z < that.z


@dataclass
class Brick:
    id: int
    p1: Coord
    p2: Coord

    def __post_init__(self):
        assert self.id != EMPTY_BRICK_ID
        p1 = self.p1
        p2 = self.p2
        if p1 > p2:
            self.p1 = p2
            self.p2 = p1


def create_empty_grid(
    bricks: list[Brick],
    dims: Literal[2, 3],
    fill_val,
) -> np.ndarray:
    coords = list(map(lambda b: b.p1, bricks)) + list(map(lambda b: b.p2, bricks))
    min_x = min(map(lambda b: b.x, coords))
    max_x = max(map(lambda b: b.x, coords))

    min_y = min(map(lambda b: b.y, coords))
    max_y = max(map(lambda b: b.y, coords))

    min_z = min(map(lambda b: b.z, coords))
    max_z = max(map(lambda b: b.z, coords))
    assert min_x >= 0
    assert min_y >= 0
    assert min_z >= 0

    if dims == 2:
        shape = (max_x + 1, max_y + 1)
    elif dims == 3:
        shape = (max_x + 1, max_y + 1, max_z + 1)
    else:
        raise ValueError
    return np.full(shape, fill_val)


def process_bricks(bricks: list[Brick]):
    # key is brick that is above, value is list of bricks that support key
    bricks_below_map: dict[int, set[int]] = dict()

    height_grid = create_empty_grid(bricks, dims=2, fill_val=0)
    brick_grid = create_empty_grid(bricks, dims=3, fill_val=EMPTY_BRICK_ID)
    # order by what will be below based on height
    bricks = sorted(bricks, key=lambda b: b.p1.z)

    for brick in bricks:
        x_slice = slice(brick.p1.x, brick.p2.x + 1)
        y_slice = slice(brick.p1.y, brick.p2.y + 1)
        support_height = np.max(height_grid[x_slice, y_slice])
        support_bricks = set(
            brick_grid[x_slice, y_slice, support_height].flatten().tolist()
        ) - {EMPTY_BRICK_ID}
        bricks_below_map[brick.id] = support_bricks
        new_start_z = support_height + 1
        new_end_z = new_start_z + (brick.p2.z - brick.p1.z)
        height_grid[x_slice, y_slice] = new_end_z
        brick_grid[x_slice, y_slice, new_start_z : new_end_z + 1] = brick.id

    return bricks_below_map, brick_grid


def parse_brick(id, s) -> Brick:
    p1_str, p2_str = s.split("~", 1)
    p1 = [int(i) for i in p1_str.split(",", 2)]
    p2 = [int(i) for i in p2_str.split(",", 2)]
    return Brick(
        id,
        p1=Coord(p1[0], p1[1], p1[2]),
        p2=Coord(p2[0], p2[1], p2[2]),
    )


def parse_file(fname) -> list[Brick]:
    bricks = []
    with open(fname) as f:
        for i, line in enumerate(f):
            line = line.strip()
            bricks.append(parse_brick(i, line))
    return bricks


def part1(bricks_below_map: dict[int, set[int]]) -> None:
    cannot_remove_set = set()
    for above, belows in bricks_below_map.items():
        if len(belows) == 1:
            cannot_remove_set.add(next(iter(belows)))
    return set(i for i in bricks_below_map) - cannot_remove_set


def part2(bricks_below_map: dict[int, set[int]]) -> int:
    total = 0
    brick_ids = list(bricks_below_map.keys())
    for brick_id in brick_ids:
        total += get_bricks_to_fall_count(brick_id, copy.deepcopy(bricks_below_map))
    return total


def get_bricks_to_fall_count(brick_id, bricks_below_map):
    count = 0
    bricks_to_fall = [brick_id]
    while len(bricks_to_fall) > 0:
        brick_to_fall = bricks_to_fall.pop()
        for above, belows in bricks_below_map.items():
            if brick_to_fall in belows:
                belows.remove(brick_to_fall)
                if len(belows) == 0:
                    count += 1
                    bricks_to_fall.append(above)
    return count


if __name__ == "__main__":
    bricks = parse_file("y2023/data/d22_small.txt")
    bricks = parse_file("y2023/data/d22.txt")
    bricks_below_map, _ = process_bricks(bricks)
    len(part1(bricks_below_map))
    part2(bricks_below_map)
