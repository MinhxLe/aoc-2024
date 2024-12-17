from dataclasses import dataclass
from os import WCOREDUMP
import re
import math

"""
ax + by = c minimizing 3a+b
a and b are integers

TODO: would be cool to learn integer programming
"""


class M2(list[list[int]]):
    def __post_init__(self) -> None:
        # TODO this is not working
        assert len(self) == 2
        assert all([len(x) == 2 for x in self])


class V2(list[int]):
    def __post_init__(self) -> None:
        # TODO this is not working
        assert len(self) == 2


def determinant(m: M2) -> int:
    return (m[0][0] * m[1][1]) - (m[0][1] * m[1][0])


def null_space(m: M2) -> V2:
    d = math.gcd(m[0][0], m[0][1])
    return V2([-m[0][1] // d, m[1][1] // d])


def find_solution(m: M2, v: V2) -> V2 | None:
    # cramer's rule (?)
    det = determinant(m)
    n1 = v[0] * m[1][1] - v[1] * m[0][1]
    n2 = v[1] * m[0][0] - v[0] * m[1][0]

    if (n1 % det) != 0 or (n2 % det) != 0:
        return None
    candidate = V2([n1 // det, n2 // det])
    # TODO this is not the minimum candidate
    return candidate


@dataclass
class Problem:
    button_a: V2
    button_b: V2
    target: V2


def solve_part_1(problem: Problem) -> int | None:
    button_a = problem.button_a
    button_b = problem.button_b
    target = problem.target
    M = M2(
        [
            [button_a[0], button_b[0]],
            [button_a[1], button_b[1]],
        ]
    )
    v = find_solution(M, target)
    if v is not None:
        assert v[0] >= 0
        assert v[1] >= 0
        return v[0] * 3 + v[1]
    else:
        return None


def solve_part_2(problem: Problem) -> int | None:
    button_a = problem.button_a
    button_b = problem.button_b
    target = problem.target
    offset = 10_000_000_000_000
    target_offset = V2([target[0] + offset, target[1] + offset])
    M = M2(
        [
            [button_a[0], button_b[0]],
            [button_a[1], button_b[1]],
        ]
    )
    v = find_solution(M, target_offset)
    if v is not None:
        assert v[0] >= 0
        assert v[1] >= 0
        return v[0] * 3 + v[1]
    else:
        return None


def parse_problems(fname: int) -> list[Problem]:
    with open(fname) as f:
        text = f.read()

    # Split text into individual game states
    sections = text.strip().split("\n\n")
    problems = []

    for section in sections:
        button_a = None
        button_b = None
        target = None
        # Process each line
        lines = section.strip().split("\n")

        a_match = re.search(r"Button A: X\+(\d+), Y\+(\d+)", lines[0])
        if a_match:
            button_a = V2([int(a_match.group(1)), int(a_match.group(2))])

        # Parse Button B
        b_match = re.search(r"Button B: X\+(\d+), Y\+(\d+)", lines[1])
        if b_match:
            button_b = V2([int(b_match.group(1)), int(b_match.group(2))])

        # Parse Prize
        p_match = re.search(r"Prize: X=(\d+), Y=(\d+)", lines[2])
        if p_match:
            target = V2([int(p_match.group(1)), int(p_match.group(2))])
        assert button_a is not None
        assert button_b is not None
        assert target is not None
        problems.append(Problem(button_a, button_b, target))
    return problems


# test problem 1
def test_1():
    A = M2([[94, 22], [34, 67]])
    y = V2([8400, 5400])
    z = V2([3, 1])

    print(find_solution(A, y))


def test_2():
    A = M2([[26, 67], [66, 21]])
    y = V2([12748, 12176])
    z = V2([3, 1])

    print(find_solution(A, y))


def test_3():
    A = M2([[17, 84], [86, 37]])
    y = V2([7870, 6450])
    z = V2([3, 1])
    print(find_solution(A, y))


def test_4():
    A = M2([[69, 27], [23, 71]])
    y = V2([18641, 10279])
    z = V2([3, 1])
    print(find_solution(A, y))


test_1()
test_2()
test_3()
test_4()
problems = parse_problems("data/day13.txt")
solutions_1 = [solve_part_1(p) for p in problems]
solutions_2 = [solve_part_2(p) for p in problems]
