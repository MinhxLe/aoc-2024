def parse_file(fname) -> list[list[int]]:
    with open(fname) as f:
        content = f.read()
    group_strs = content.split("\n\n")
    groups = []
    for group_str in group_strs:
        group = [int(n) for n in group_str.split("\n") if n]
        groups.append(group)
    return groups


def p1(groups: list[list[int]]):
    return max(map(sum, groups))


def p2(groups: list[list[int]]):
    sorted_sums = sorted(list(map(sum, groups)), reverse=True)
    return sum(sorted_sums[:3])


if __name__ == "__main__":
    fname = "y2022/data/d1.txt"
    groups = parse_file(fname)
    p1(groups)
