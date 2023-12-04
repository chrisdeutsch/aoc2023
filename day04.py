import re
import heapq
from dataclasses import dataclass


@dataclass
class Card:
    card_num: int
    num_matches: int


def parse_cards(inputs: str):
    pattern = re.compile(r"^Card\s+(\d+):\s+(.+)\s\|\s(.+)$")
    for line in inputs.splitlines():
        m = pattern.match(line)
        card_num = int(m.group(1))
        winning_nums = set(m.group(2).split())
        nums = set(m.group(3).split())

        num_matches = len(winning_nums.intersection(nums))
        yield Card(card_num, num_matches)


def part1(inputs: str):
    total_points = 0
    for card in parse_cards(inputs):
        if card.num_matches > 0:
            total_points += 2 ** (card.num_matches - 1)

    return total_points


def part2(inputs: str):
    original_cards = list(parse_cards(inputs))

    total_cards = len(original_cards)
    stack = original_cards.copy()
    while len(stack) > 0:
        card = stack.pop()
        for i in range(card.card_num + 1, card.card_num + card.num_matches + 1):
            stack.append(original_cards[i - 1])
            total_cards += 1

    return total_cards


TEST_INPUT = """\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""


def test_part1():
    assert part1(TEST_INPUT) == 13


def test_part2():
    assert part2(TEST_INPUT) == 30


if __name__ == "__main__":
    with open("inputs/day04.txt") as fin:
        inputs = fin.read()

    print(f"Part 1: {part1(inputs)}")
    print(f"Part 2: {part2(inputs)}")