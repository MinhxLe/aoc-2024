from dataclasses import dataclass


@dataclass
class Card:
    id: int
    winning_nums: list[int]
    nums: list[int]

    def score(self) -> int:
        n_matches = self.n_matches()
        if n_matches == 0:
            return 0
        else:
            return 2 ** (n_matches - 1)

    def n_matches(self) -> int:
        n_matches = 0
        for num in self.nums:
            if num in self.winning_nums:
                n_matches += 1
        return n_matches


def parse_card(s) -> Card:
    id_str, card_str = s.split(": ", 1)
    id = int(id_str[len("Card ") :])
    card_str = card_str.strip()
    winning_nums_str, nums_str = card_str.split(" | ")
    winning_nums = [int(i) for i in winning_nums_str.split(" ") if i]
    nums = [int(i) for i in nums_str.split(" ") if i]
    return Card(id, winning_nums, nums)


def parse_cards(fname) -> list[Card]:
    cards = []
    with open(fname) as f:
        for line in f:
            cards.append(parse_card(line.strip()))
    return cards


def p1():
    cards = parse_cards("./y2023/data/d4.txt")
    print(sum([c.score() for c in cards]))


def p2():
    cards = parse_cards("./y2023/data/d4.txt")
    n_cards = [1 for _ in range(len(cards))]
    for i, card in enumerate(cards):
        for i_prime in range(i + 1, i + card.n_matches() + 1):
            n_cards[i_prime] += n_cards[i]
    print(sum(n_cards))
