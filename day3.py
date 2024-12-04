import re


def compute(text: str) -> int:
    pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
    matches = re.findall(pattern, text)
    total = 0
    for num1, num2 in matches:
        total += int(num1) * int(num2)
    return total


DO = "do()"
DONT = "don't()"


def compute2(text: str) -> int:
    total = 0
    text = "do()" + text
    for subtext in text.split("don't()"):
        if "do()" in subtext:
            total += compute(subtext[subtext.index("do()") :])
    return total


with open("data/day3.txt") as f:
    text = f.read()

# print(compute(text))
print(compute2(text))
print(
    compute2(
        "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    )
)
