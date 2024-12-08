from dataclasses import dataclass
import functools
from typing import Tuple
import re


@dataclass(frozen=True)
class PageRule:
    n1: int
    n2: int


def sort_update(
    updates: list[int],
    rules: list[PageRule],
) -> list[int]:
    rule_set = set(rules)

    def cmp(x: int, y: int):
        if PageRule(x, y) in rule_set:
            return -1
        elif PageRule(y, x) in rule_set:
            return 1
        else:
            return 0

    return sorted(updates, key=functools.cmp_to_key(cmp))


assert sort_update([1, 2], []) == [1, 2]
assert sort_update([1, 2], [PageRule(2, 1)]) == [2, 1]
assert sort_update([1, 2], [PageRule(2, 1)]) == [2, 1]


def read_inputs() -> Tuple[list[PageRule], list[list[int]]]:
    rules, updates = [], []
    with open("data/day5.txt") as f:
        for line in f:
            if (match := re.match(r"(\d+)\|(\d+)", line)) is not None:
                n1, n2 = match.groups()
                rules.append(PageRule(int(n1), int(n2)))
            elif re.match(r"[\d,]+\d", line) is not None:
                nums = line.split(",")
                updates.append([int(n) for n in nums])
    return rules, updates


def is_valid_page_order(updates: list[int], rules: list[PageRule]) -> bool:
    rule_set = {r for r in rules}
    for i in range(len(updates)):
        for j in range(i, len(updates)):
            if PageRule(updates[j], updates[i]) in rule_set:
                return False
    return True


def part_1(updates: list[list[int]], rules: list[PageRule]):
    total = 0
    for update in updates:
        if is_valid_page_order(update, rules):
            total += update[len(update) // 2]
    return total


def part_2(updates: list[list[int]], rules: list[PageRule]):
    total = 0
    for update in updates:
        if not is_valid_page_order(update, rules):
            sorted_update = sort_update(update, rules)
            total += sorted_update[len(sorted_update) // 2]
    return total


rules, updates = read_inputs()
print(part_2(updates, rules))
