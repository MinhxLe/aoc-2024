import re
from dataclasses import dataclass
from typing import Counter, Tuple
from utils import V2


def print_positions(positions: list[V2], max_x: int, max_y: int) -> None:
    grid = [["." for _ in range(max_y)] for _ in range(max_x)]
    for position in positions:
        grid[position.x][position.y] = "*"
    for line in grid:
        print(*line)


def calculate_final_position(p0: V2, v: V2, t: int, max_x: int, max_y: int) -> V2:
    p_final = p0 + (t * v)

    return V2(
        p_final.x % max_x,
        p_final.y % max_y,
    )


def get_quadrant(p: V2, max_x: int, max_y: int) -> Tuple[int, int] | None:
    mid_x = max_x // 2
    mid_y = max_y // 2

    if p.x == mid_x or p.y == mid_y:
        return None

    quadrant_x = 0 if p.x < mid_x else 1
    quadrant_y = 0 if p.y < mid_y else 1
    return (quadrant_x, quadrant_y)


@dataclass
class InitialState:
    p0: V2
    v: V2


@dataclass
class Problem:
    robot_states: list[InitialState]
    max_x: int
    max_y: int
    t: int


def part_1(problem: Problem) -> int:
    quadrants = []
    for state in problem.robot_states:
        final_position = calculate_final_position(
            state.p0,
            state.v,
            problem.t,
            problem.max_x,
            problem.max_y,
        )
        quadrant = get_quadrant(
            final_position,
            problem.max_x,
            problem.max_y,
        )
        if quadrant is not None:
            quadrants.append(quadrant)

    counter = Counter(quadrants)
    total = 1
    for v in counter.values():
        total *= v
    return total


def parse_problem(fname: str) -> Problem:
    def parse_line(line):
        # Extract all numbers (including negative) using regex
        numbers = re.findall(r"-?\d+", line)
        # Convert strings to integers
        return [int(num) for num in numbers]

    with open(fname) as f:
        lines = [x.strip() for x in f]

    robot_states = []
    for line in lines:
        px, py, vx, vy = parse_line(line)
        robot_states.append(InitialState(V2(px, py), V2(vx, vy)))
    return Problem(
        robot_states=robot_states,
        t=100,
        max_x=101,
        max_y=103,
    )


test_problem = Problem(
    robot_states=[
        InitialState(p0=V2(0, 4), v=V2(3, -3)),
        InitialState(p0=V2(6, 3), v=V2(-1, -3)),
        InitialState(p0=V2(10, 3), v=V2(-1, 2)),
        InitialState(p0=V2(2, 0), v=V2(2, -1)),
        InitialState(p0=V2(0, 0), v=V2(1, 3)),
        InitialState(p0=V2(3, 0), v=V2(-2, -2)),
        InitialState(p0=V2(7, 6), v=V2(-1, -3)),
        InitialState(p0=V2(3, 0), v=V2(-1, -2)),
        InitialState(p0=V2(9, 3), v=V2(2, 3)),
        InitialState(p0=V2(7, 3), v=V2(-1, 2)),
        InitialState(p0=V2(2, 4), v=V2(2, -3)),
        InitialState(p0=V2(9, 5), v=V2(-3, -3)),
    ],
    max_x=11,
    max_y=7,
    t=100,
)


def part_2(problem: Problem, start_t, end_t: int | None = None):
    if end_t is None:
        end_t = start_t + 5
    for t in range(start_t, end_t, 50):
        final_positions = [
            calculate_final_position(
                x.p0, x.v, max_x=problem.max_x, max_y=problem.max_y, t=t
            )
            for x in problem.robot_states
        ]
        print(f"iteration {t}")
        print_positions(final_positions, problem.max_x, problem.max_y)


problem = parse_problem("data/day14.txt")
# print(part_1(test_problem))
# print(part_1(problem))

part_2(problem, 500, 10000)
