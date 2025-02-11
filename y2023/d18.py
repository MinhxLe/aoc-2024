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
        pattern = r"(\w) (\d+) \(#.*\)"
        for line in f:
            match = re.match(pattern, line)
            assert match is not None
            direction_str, n_step_str  = match.groups()
            instructions.append(
                Instruction(
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


def parse_instructions_2(fname) -> list[Instruction]:
    instructions = []
    with open(fname) as f:
        pattern = r"\w \d+ \((#.*)\)"
        for line in f:
            match = re.match(pattern, line)
            assert match is not None
            hex_str = match.groups()
            n_steps = ...
            direction = dict(
                0=DirectionEnum.EAST,
                1=DirectionEnum.SOUTH,
                2=DirectionEnum.WEST,
                3=DirectionEnum.NORTH,
            )[hex_str[-1]]
            instructions.append(
                Instruction(
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


def compute_area(vertices: list[V2]) -> int:
    # shoelace formula, trapezoid formula
    area = 0
    n = len(vertices)
    for i in range(n):
        p = vertices[i]
        next_p = vertices[(i + 1) % n]
        area += (p.y + next_p.y) * (p.x - next_p.x) // 2
    return abs(area)


def is_left(p1: V2, p2: V2, orrientation: DirectionEnum) -> bool:
    match orrientation:
        case DirectionEnum.NORTH:
            return p1.x < p2.x
        case DirectionEnum.SOUTH:
            return p1.x > p2.x
        case DirectionEnum.EAST:
            return p1.y > p2.y
        case DirectionEnum.WEST:
            return p1.y < p2.y
    raise ValueError


def get_boundary_vertices(instructions: list[Instruction]) -> Tuple[list[V2], list[V2]]:
    # The initial points of the front digger if it was facing north
    # we want p2 to be left of p1
    orrientation = instructions[0].direction
    right_p = V2(0, 0)
    left_p = right_p + orrientation.counter_clockwise().to_v2()
    assert is_left(left_p, right_p, orrientation)
    vs1, vs2 = [right_p], [left_p]
    for i, instruction in enumerate(instructions):
        orrientation = instruction.direction
        assert is_left(left_p, right_p, orrientation)
        next_instruction = instructions[(i + 1) % len(instructions)]
        right_p += instruction.n_steps * orrientation.to_v2()
        left_p += instruction.n_steps * orrientation.to_v2()
        # turn right next
        if orrientation.clockwise() == next_instruction.direction:
            vs2.append(left_p)
            left_p += orrientation.clockwise().to_v2()
            right_p -= orrientation.to_v2()
            vs1.append(right_p)
        # turn left next
        elif orrientation.counter_clockwise() == next_instruction.direction:
            vs1.append(right_p)
            right_p += orrientation.counter_clockwise().to_v2()
            left_p -= orrientation.to_v2()
            vs2.append(left_p)
        else:
            raise ValueError()

    return vs1, vs2


if __name__ == "__main__":
    # fname = "y2023/data/d18_small.txt"
    fname = "y2023/data/d18.txt"
    instructions = parse_instructions(fname)
    vs1, vs2 = get_boundary_vertices(instructions)
