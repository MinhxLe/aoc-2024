from dataclasses import dataclass
import string
from os_utils import parse_file


@dataclass
class Bag:
    slot1: str
    slot2: str


def item_priority(item: str) -> int:
    assert item in string.ascii_letters
    if item in string.ascii_lowercase:
        return ord(item) - ord("a") + 1
    elif item in string.ascii_uppercase:
        return ord(item) - ord("A") + 27
    else:
        raise ValueError


def find_common_items(bag: Bag) -> list[str]:
    return list(set(bag.slot1) & set(bag.slot2))


def p1(bags: list[Bag]) -> int:
    total = 0
    for bag in bags:
        print(
            find_common_items(bag), [item_priority(i) for i in find_common_items(bag)]
        )
        total += sum([item_priority(i) for i in find_common_items(bag)])
    return total


def find_common_items_within_bags(bags: list[Bag]) -> list[str]:
    if len(bags) == 0:
        return []
    common_items = set(bags[0].slot1) | set(bags[0].slot2)
    for bag in bags:
        common_items &= set(bag.slot1) | set(bag.slot2)
    return list(common_items)


def p2(bags: list[Bag], group_size: int) -> int:
    assert len(bags) % group_size == 0
    total = 0
    for i in range(0, len(bags), group_size):
        grouped_bags = bags[i : i + group_size]
        common_items = find_common_items_within_bags(grouped_bags)
        assert len(common_items) == 1
        total += item_priority(common_items[0])
    return total


def parse_bag(s: str) -> Bag:
    return Bag(
        slot1=s[: len(s) // 2],
        slot2=s[len(s) // 2 :],
    )


if __name__ == "__main__":
    test_bags = parse_file("y2022/data/d3_small.txt", parse_bag)
    bags = parse_file("y2022/data/d3.txt", parse_bag)
    p1(bags)
    p2(test_bags, 3)
    p2(bags, 3)
