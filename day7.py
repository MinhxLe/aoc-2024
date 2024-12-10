from typing import Literal
from dataclasses import dataclass


@dataclass
class Problem:
    target: int
    numbers: list[int]


def find_valid_equation(
    target: int,
    numbers: list[int],
) -> list[Literal["*", "+"]] | None:
    if target < 0:
        return None
    if len(numbers) == 0:
        return None
    elif len(numbers) == 1:
        return [] if numbers[0] == target else None
    sub_equation = None
    if (
        sub_equation := find_valid_equation(target - numbers[-1], numbers[:-1])
    ) is not None:
        sub_equation.append("+")
    elif (target % numbers[-1]) == 0 and (
        sub_equation := find_valid_equation(target // numbers[-1], numbers[:-1])
    ) is not None:
        sub_equation.append("*")
    else:
        number_str = str(numbers[-1])
        target_str = str(target)
        number_str_length = len(number_str)
        if (
            len(target_str) > len(number_str)
            and target_str[-number_str_length:] == number_str
        ):
            new_target = target_str[:-number_str_length]
            sub_equation = find_valid_equation(int(new_target), numbers[:-1])
    return sub_equation


assert find_valid_equation(190, [10, 19]) == ["*"]
assert find_valid_equation(292, [11, 6, 16, 20]) == ["+", "*", "+"]
assert find_valid_equation(3267, [81, 40, 27]) == ["*", "+"]


def part_1(problems: list[Problem]) -> int:
    total = 0
    for problem in problems:
        if find_valid_equation(problem.target, problem.numbers) is not None:
            total += problem.target
    return total


problems = []
with open("data/day7.txt") as f:
    for line in f:
        target, numbers = line.split(": ")
        target = int(target)
        numbers = numbers.split(" ")
        numbers = [int(n) for n in numbers]
        problems.append(Problem(target, numbers))

print(part_1(problems))
