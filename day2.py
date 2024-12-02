DATA_FILE = "./data/day2.txt"


def get_input() -> list[list[int]]:
    numbers = []
    with open(DATA_FILE, "r") as f:
        for line in f:
            numbers.append([int(x) for x in line.split()])
    return numbers


def is_level_safe(levels: list[int]) -> bool:
    if len(levels) == 0:
        return True
    if len(levels) == 1:
        return True

    is_safe = True
    mode = None
    for i in range(0, len(levels) - 1):
        if mode is None:
            if levels[i] < levels[i + 1]:
                mode = "inc"
            else:
                mode = "dec"
        else:
            if mode == "inc":
                is_safe &= levels[i] < levels[i + 1]
            elif mode == "dec":
                is_safe &= levels[i] > levels[i + 1]
            else:
                raise ValueError
        is_safe &= 1 <= abs(levels[i] - levels[i + 1]) <= 3

    return is_safe


def is_level_safe_with_dampener(levels: list[int]) -> bool:
    for i in range(0, len(levels)):
        if is_level_safe(levels[:i] + levels[i + 1 :]):
            return True
    return False


assert is_level_safe([])
assert is_level_safe([1])
assert is_level_safe([1, 2, 3])
assert is_level_safe([3, 2, 1])
assert not is_level_safe([1, 1])
assert not is_level_safe([1, 2, 1])
assert not is_level_safe([1, 2, 1])
assert not is_level_safe([1, 5])
assert not is_level_safe([5, 1])

number_lists = get_input()
print(len([x for x in number_lists if is_level_safe(x)]))
print(len([x for x in number_lists if is_level_safe_with_dampener(x)]))
