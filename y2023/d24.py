from dataclasses import dataclass
import numpy as np
from numpy.linalg import LinAlgError
import math


@dataclass
class R2:
    x: float
    y: float


@dataclass
class R3:
    x: float
    y: float
    z: float


@dataclass
class State:
    p0: R3
    v: R3


"""
p(t) = p0 + vt
does there exist a t1 and t2 such that where t1 and t2 are >= 0
pa0 + vat1 = pb0 + vbt2

(pa0 - pb0) + vat1 - vbt2 = 0


There are 3 scenarios
1. parallel, exact same line
2. parallel, not same line
3.  not parallel.
  if not parallel, you solve for x, y and validate the z axis will work



x1 + vx1*t1 = x2 +vx2*t2
y1 + vy1*t1 = y2 +vy2*t2


vx1 t1 - vx2 t2 = x2 - x1
vx1 t1 - vx2 t2 = x2 - x1
"""


def solve(
    s1: State,
    s2: State,
):
    # solving for a valid x and y such that
    # x1 + vx1*t1 = x2 +vx2*t2
    # y1 + vy1*t1 = y2 +vy2*t2
    a = np.array(
        [
            [s1.v.x, -s2.v.x],
            [s1.v.y, -s2.v.y],
        ]
    )
    b = np.array(
        [
            s2.p0.x - s1.p0.x,
            s2.p0.y - s1.p0.y,
        ]
    )
    try:
        return np.linalg.solve(a, b)
    except LinAlgError:
        return None


def find_intersection(
    s1: State,
    s2: State,
) -> R2 | None:
    if s1.v == s2.v:
        # not technically correct
        return None
    else:
        valid_times = solve(s1, s2)
        if valid_times is not None and np.all(valid_times >= 0):
            t1, t2 = valid_times
            return R2(
                x=t1 * s1.v.x + s1.p0.x,
                y=t1 * s1.v.y + s1.p0.y,
            )
            # given the times which x and y coords match, we want to see if
            # the z cooridinate also match
            # if math.isclose(t1 * s1.v.z + s1.p0.z, t2 * s2.v.z + s2.p0.z):
            #     return R3(
            #         x=t1 * s1.v.x * t1,
            #         y=t1 * s1.v.y * t1,
            #         z=t1 * s1.v.z * t1,
            #     )
            # else:
            #     return None


def part1(
    states: list[State],
    min_value: float,
    max_value: float,
) -> int:
    count = 0
    for i in range(len(states)):
        for j in range(i + 1, len(states)):
            s1, s2 = states[i], states[j]
            intersection = find_intersection(s1, s2)
            if (
                intersection is not None
                and min_value <= intersection.x <= max_value
                and min_value <= intersection.y <= max_value
            ):
                count += 1
    return count


def parse_r3(s) -> R3:
    x, y, z = s.split(", ", 2)
    return R3(
        x=float(x),
        y=float(y),
        z=float(z),
    )


def parse_state(s) -> State:
    p0_str, v0_str = s.split(" @ ", 1)
    return State(
        p0=parse_r3(p0_str),
        v=parse_r3(v0_str),
    )


def test_find_intersection():
    a = parse_state("19, 13, 30 @ -2, 1, -2")
    b = parse_state("18, 19, 22 @ -1, -1, -2")
    find_intersection(a, b)


def parse_file(fname) -> list[State]:
    states = []
    with open(fname) as f:
        for line in f:
            line = line.strip()
            states.append(parse_state(line))
    return states


if __name__ == "__main__":
    states = parse_file("./y2023/data/d24_small.txt")
    part1(states, 7, 27)

    states = parse_file("./y2023/data/d24.txt")
    part1(states, 200000000000000, 400000000000000)
