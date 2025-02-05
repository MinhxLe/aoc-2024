import string
from utils import first


def parse_p1(s) -> int:
    d1 = first(s, lambda c: c in string.digits)
    d2 = first(reversed(s), lambda c: c in string.digits)
    return int(d1 + d2)


def parse_first_num(s, reversed: bool):
    key_to_val = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }
    for i in range(1, 10):
        key_to_val[str(i)] = i
    if reversed:
        s = s[::-1]
    for i in range(len(s)):
        for key, val in key_to_val.items():
            if reversed:
                key = key[::-1]
            if s[i : i + len(key)] == key:
                return val
    raise ValueError("could not find number")


def parse_p2(s) -> int:
    d1 = parse_first_num(s, False)
    d2 = parse_first_num(s, True)
    return int(str(d1) + str(d2))


def part1(fname):
    nums = []
    with open(fname) as f:
        for line in f:
            nums.append(parse_p1(line))
    print(sum(nums))


def part2(fname):
    nums = []
    with open(fname) as f:
        for line in f:
            nums.append(parse_p2(line))
    print(sum(nums))


if __name__ == "__main__":
    part1("./y2023/data/d1.txt")
    part2("./y2023/data/d1.txt")
