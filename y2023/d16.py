import functools
from dataclasses import dataclass
from typing import Literal

from grid import V2, DirectionEnum, Grid, read_grid


@dataclass(frozen=True)
class Ray:
    p: V2
    dir: DirectionEnum

    def move(self, dir) -> "Ray":
        return Ray(self.p + dir.to_v2(), dir)


def get_next_rays(
    ray: Ray,
    tile: Literal["|", "/", "\\", "-", "."],
) -> list[Ray]:
    if tile == "|":
        if ray.dir in [DirectionEnum.EAST, DirectionEnum.WEST]:
            next_dirs = [DirectionEnum.NORTH, DirectionEnum.SOUTH]
        else:
            next_dirs = [ray.dir]
    elif tile == "-":
        if ray.dir in [DirectionEnum.NORTH, DirectionEnum.SOUTH]:
            next_dirs = [DirectionEnum.WEST, DirectionEnum.EAST]
        else:
            next_dirs = [ray.dir]
    elif tile == "\\":
        next_dirs = [
            {
                DirectionEnum.NORTH: DirectionEnum.WEST,
                DirectionEnum.SOUTH: DirectionEnum.EAST,
                DirectionEnum.WEST: DirectionEnum.NORTH,
                DirectionEnum.EAST: DirectionEnum.SOUTH,
            }[ray.dir]
        ]
    elif tile == "/":
        next_dirs = [
            {
                DirectionEnum.NORTH: DirectionEnum.EAST,
                DirectionEnum.SOUTH: DirectionEnum.WEST,
                DirectionEnum.WEST: DirectionEnum.SOUTH,
                DirectionEnum.EAST: DirectionEnum.NORTH,
            }[ray.dir]
        ]
    elif tile == ".":
        next_dirs = [ray.dir]
    else:
        raise ValueError
    return [ray.move(dir) for dir in next_dirs]


def get_energized_tiles(start_ray: Ray, grid: Grid):
    visited = {start_ray}
    rays = {start_ray}

    while len(rays) > 0:
        ray = rays.pop()
        next_rays = get_next_rays(ray, grid.at(ray.p))
        for next_ray in next_rays:
            if next_ray not in visited and grid.is_inbounds(next_ray.p):
                visited.add(next_ray)
                rays.add(next_ray)

    return {r.p for r in visited}


def p2(grid: Grid):
    max_energized = 0
    for x in range(0, grid.height):
        max_energized = max(
            max_energized,
            len(get_energized_tiles(Ray(V2(x, 0), DirectionEnum.EAST), grid)),
        )
        max_energized = max(
            max_energized,
            len(
                get_energized_tiles(
                    Ray(V2(x, grid.width - 1), DirectionEnum.WEST), grid
                )
            ),
        )
    for y in range(0, grid.width):
        max_energized = max(
            max_energized,
            len(get_energized_tiles(Ray(V2(0, y), DirectionEnum.SOUTH), grid)),
        )
        max_energized = max(
            max_energized,
            len(
                get_energized_tiles(
                    Ray(V2(grid.height - 1, y), DirectionEnum.NORTH), grid
                )
            ),
        )
    return max_energized


if __name__ == "__main__":
    test_grid = read_grid("./y2023/data/d16_small.txt")
    grid = read_grid("./y2023/data/d16.txt")
    # part 1
    start_ray = Ray(V2(0, 0), DirectionEnum.EAST)
    print(len(get_energized_tiles(start_ray, grid)))
