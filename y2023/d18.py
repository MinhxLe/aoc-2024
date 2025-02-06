from typing import Tuple
from grid import DirectionEnum, GridV2, V2
from dataclasses import dataclass
import re
import matplotlib.pyplot as plt
import numpy as np
import copy

MAX_GRID = 1_000


@dataclass
class Instruction:
    direction: DirectionEnum
    n_steps: int
    color: str


def create_trench_boundary(
    instructions: list[Instruction],
    ground_size: int,
) -> GridV2[bool]:
    trench = GridV2.fill(False, ground_size, ground_size)
    p = V2(ground_size // 2, ground_size // 2)
    trench[p.x][p.y] = True
    for instruction in instructions:
        for _ in range(instruction.n_steps):
            p += instruction.direction.to_v2()
            trench.update(p, True)
    return trench


def is_interior(p: V2, boundary: GridV2[bool]) -> bool:
    if not boundary.is_inbounds(p):
        return False
    if boundary.at(p):
        return False
    for direction in DirectionEnum:
        found_boundary = False
        curr_p = p
        while boundary.is_inbounds(curr_p):
            if boundary.at(curr_p) is True:
                found_boundary = True
                break
            else:
                curr_p += direction.to_v2()
        if not found_boundary:
            return False
    return True


def find_interior_point(boundary: GridV2[bool]) -> V2 | None:
    for i in range(boundary.height):
        for j in range(boundary.width):
            if is_interior(V2(i, j), boundary):
                return V2(i, j)
    return None


def fill_trench_boundary(boundary: GridV2[bool]):
    trench = copy.deepcopy(boundary)
    interior_p = find_interior_point(trench)
    assert interior_p is not None

    node_queue = [interior_p]
    trench.update(interior_p, True)
    while len(node_queue) > 0:
        p = node_queue.pop()
        for direction in DirectionEnum:
            new_p = p + direction.to_v2()
            if trench.is_inbounds(new_p) and not trench.at(new_p):
                trench.update(new_p, True)
                node_queue.append(new_p)
    return trench


def save_trench_img(trench):
    np.array(trench)
    plt.imshow(np.array(trench), cmap="binary")
    plt.axis("off")
    plt.savefig("/tmp/trench.png")


def parse_instructions(fname) -> list[Instruction]:
    instructions = []
    with open(fname) as f:
        pattern = r"(\w) (\d+) \((#.*)\)"
        for line in f:
            match = re.match(pattern, line)
            assert match is not None
            direction_str, n_step_str, color_str = match.groups()
            instructions.append(
                Instruction(
                    color=color_str,
                    n_steps=int(n_step_str),
                    direction=dict(
                        R=DirectionEnum.EAST,
                        L=DirectionEnum.WEST,
                        U=DirectionEnum.NORTH,
                        D=DirectionEnum.SOUTH,
                    )[direction_str],
                )
            )
    return instructions


def get_interior_vertices(instructions: list[Instruction]) -> list[V2]:
    # we are digging a trench starting with a whole at 0, 0
    # we can think of it as 4 points on cartesian coordinates. only 1 of these points will
    # eventually reconnect. That set of vertices is the interior boundary of the polygon
    vertices = [V2(0, 0)]
    for instruction in instructions:
        vertices.append(
            vertices[-1] + (instruction.n_steps * instruction.direction.to_v2())
        )
    assert vertices[0] == vertices[-1]
    return vertices[:-1]


def get_boundary_vertices(instructions: list[Instruction]) -> list[V2]:
    vertices = [V2(0, 0)]
    for instruction in instructions:
        vertices.append(
            vertices[-1] + (instruction.n_steps * instruction.direction.to_v2())
        )
    assert vertices[0] == vertices[-1]
    vertices = vertices[:-1]
    return vertices


def is_above(p1: V2, p2: V2) -> bool:
    return p1.x == p2.x and p1.y > p2.y


def is_below(p1: V2, p2: V2) -> bool:
    return p1.x == p2.x and p1.y < p2.y


def is_right(p1: V2, p2: V2) -> bool:
    return p1.y == p2.y and p1.x > p2.x


def is_left(p1: V2, p2: V2) -> bool:
    return p1.y == p2.y and p1.x < p2.x


def is_adjacent(p1: V2, p2: V2) -> bool:
    return is_left(p1, p2) or is_right(p1, p2) or is_below(p1, p2) or is_above(p1, p2)


def compute_dv(p: V2, prev_p: V2, next_p: V2) -> V2:
    if is_above(prev_p, p) and is_right(next_p, p):
        dx, dy = -1, -1
    elif is_above(next_p, p) and is_right(prev_p, p):
        dx, dy = 1, 1
    elif is_below(prev_p, p) and is_right(next_p, p):
        dx, dy = 1, -1
    elif is_below(next_p, p) and is_right(prev_p, p):
        dx, dy = -1, 1
    elif is_left(prev_p, p) and is_below(next_p, p):
        dx, dy = -1, -1
    elif is_left(next_p, p) and is_below(prev_p, p):
        dx, dy = 1, 1
    elif is_left(prev_p, p) and is_above(next_p, p):
        dx, dy = 1, -1
    elif is_left(next_p, p) and is_above(prev_p, p):
        dx, dy = -1, 1
    else:
        raise ValueError
    return V2(dx, dy)


def get_edge_vertices(boundary_vertices: list[V2]) -> Tuple[list[V2], list[V2]]:
    evs1 = []
    evs2 = []
    n = len(boundary_vertices)
    for i in range(n):
        tv = boundary_vertices[i]
        prev_tv = boundary_vertices[(i - 1) % n]
        next_tv = boundary_vertices[(i + 1) % n]

        dv = compute_dv(tv, prev_tv, next_tv)
        ev1 = tv + dv
        ev2 = tv - dv
        evs1.append(ev1)
        evs2.append(ev2)

    return evs1, evs2


def draw_polygon(vs: list[V2]):
    # Extract x and y coordinates
    x = [v.x for v in vs]
    y = [v.y for v in vs]
    # Add the first point at the end to close the polygon
    x.append(x[0])
    y.append(y[0])
    plt.plot(x, y, "b-")  # 'b-' means blue line
    plt.axis("equal")
    plt.grid(True)
    plt.savefig("/tmp/polygon.png")


def compute_interior_area(vertices: list[V2]) -> int:
    # shoelace formula, trapezoid formula
    area = 0
    n = len(vertices)
    for i in range(n):
        p = vertices[i]
        next_p = vertices[(i + 1) % n]
        area += (p.y + next_p.y) * (p.x - next_p.x) // 2
    return abs(area)


def compute_boundary_area(vertices: list[V2]) -> int:
    # shoelace formula, trapezoid formula
    area = 0
    n = len(vertices)
    for i in range(n):
        p = vertices[i]
        next_p = vertices[(i + 1) % n]
        if p.x == next_p.x:
            assert p.y != next_p.y
            area += abs(p.y - next_p.y)
        elif p.y == next_p.y:
            assert p.x != next_p.x
            area += abs(p.x - next_p.x)
        else:
            raise ValueError
    return area


if __name__ == "__main__":
    fname = "y2023/data/d18_small.txt"
    # fname = "y2023/data/d18.txt"
    instructions = parse_instructions(fname)
    boundary_vs = get_boundary_vertices(instructions)
    evs1, evs2 = get_edge_vertices(boundary_vs)

    n = len(boundary_vs)
    for i in range(n):
        v = boundary_vs[i]
        prev_v = boundary_vs[(i - 1) % n]
        next_v = boundary_vs[(i + 1) % n]
        if not is_adjacent(v, prev_v) or not is_adjacent(v, next_v):
            print(i, v)
