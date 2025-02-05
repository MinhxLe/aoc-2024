from collections import defaultdict


def next_secret_number(s0: int) -> int:
    s1 = ((s0 * 64) ^ s0) % 16777216
    s2 = ((s1 // 32) ^ s1) % 16777216
    s3 = ((s2 * 2048) ^ s2) % 16777216
    return s3


def nth_secret_number(s0: int, n: int) -> int:
    for _ in range(n):
        s0 = next_secret_number(s0)
    return s0


def secret_number_seq(s0, n: int) -> list[int]:
    if n == 0:
        return []
    seq = [s0]
    for _ in range(n):
        seq.append(next_secret_number(seq[-1]))
    return seq


def calculate_max_bananas(numbers):
    seqs = [secret_number_seq(s, 2_000) for s in numbers]
    prices = [get_price(s) for s in seqs]
    price_diffs = [calculate_price_diff(s) for s in prices]

    code_values = defaultdict(int)
    for price, price_diff in zip(prices, price_diffs):
        assert len(price) == len(price_diff) + 1
        for i in range(0, len(price_diff) - 3):
            key = tuple(price_diff[i : i + 4])
            code_values[key] += price[i + 4]


def calculate_code_values(s):
    seq = secret_number_seq(s, 2_000)
    prices = [n % 10 for n in seq]
    price_diffs = [prices[i] - prices[i + 1] for i in range(len(prices) - 1)]
    code_values = dict()
    for i in range(0, len(price_diffs) - 3):
        key = tuple(price_diffs[i : i + 4])
        if key not in code_values:
            code_values[key] = prices[i + 4]
    return code_values


def part1():
    with open("data/day22.txt") as f:
        numbers = [int(l.strip()) for l in f]
    total = sum([nth_secret_number(s, 2000) for s in numbers])
    print(total)


def part2():
    with open("data/day22.txt") as f:
        numbers = [int(l.strip()) for l in f]
    all_code_values = [calculate_code_values(s) for s in numbers]
    merged_code_values = defaultdict(int)
    for code_values in all_code_values:
        for k, v in code_values.items():
            merged_code_values[k] += v
    print(sorted(merged_code_values.items(), key=lambda x: -x[1])[0])
