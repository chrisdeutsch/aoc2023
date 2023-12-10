#!/usr/bin/env python
from collections import Counter
from functools import cached_property


CARD_RANK = {
    "2": 0,
    "3": 1,
    "4": 2,
    "5": 3,
    "6": 4,
    "7": 5,
    "8": 6,
    "9": 7,
    "T": 8,
    "J": 9,
    "Q": 10,
    "K": 11,
    "A": 12,
}


TYPE_RANK = {
    "High card": 0,
    "One pair": 1,
    "Two pair": 2,
    "Three of a kind": 3,
    "Full house": 4,
    "Four of a kind": 5,
    "Five of a kind": 6,
}


class Hand:
    def __init__(self, string: str):
        assert len(string) == 5
        self.string = string

    @cached_property
    def type(self):
        counter = Counter(self.string)
        counts = [count for count in sorted(counter.values())]

        if counts == [5]:
            return "Five of a kind"
        elif counts == [1, 4]:
            return "Four of a kind"
        elif counts == [2, 3]:
            return "Full house"
        elif counts == [1, 1, 3]:
            return "Three of a kind"
        elif counts == [1, 2, 2]:
            return "Two pair"
        elif counts == [1, 1, 1, 2]:
            return "One pair"
        elif counts == [1, 1, 1, 1, 1]:
            return "High card"
        else:
            raise RuntimeError("Unknown hand type")

    @cached_property
    def rank_tuple(self):
        return (TYPE_RANK[self.type],) + tuple(CARD_RANK[card] for card in self.string)

    def __str__(self):
        return self.string

    def __repr__(self):
        return f"Hand('{self.string}')"

    def __eq__(self, rhs):
        return self.string == rhs.string


def parse(inputs):
    hands_and_bids = []
    for line in inputs.splitlines():
        hand, bid = line.split()
        hand = Hand(hand)
        bid = int(bid)
        hands_and_bids.append((hand, bid))

    return hands_and_bids


def part1(inputs):
    hands_and_bids = parse(inputs)

    total_winnings = 0
    for rank, (hand, bid) in enumerate(
        sorted(hands_and_bids, key=lambda x: x[0].rank_tuple), 1
    ):
        total_winnings += rank * bid

    return total_winnings


def part2(inputs):
    hands_and_bids = parse(inputs)

    # Determine the best hands
    best_hands = []
    for hand, bid in hands_and_bids:
        rank_tuple = tuple(
            map(lambda x: -1 if x == CARD_RANK["J"] else x, hand.rank_tuple)
        )

        possible_hands = (
            Hand(str(hand).replace("J", replacement)) for replacement in "23456789TQKA"
        )

        best_hand = max(possible_hands, key=lambda h: h.rank_tuple[0])
        best_hand_rank_tuple = (best_hand.rank_tuple[0],) + rank_tuple[1:]

        best_hands.append((best_hand, bid, best_hand_rank_tuple))

    total_winnings = 0
    for rank, (hand, bid, _) in enumerate(sorted(best_hands, key=lambda x: x[2]), 1):
        total_winnings += rank * bid

    return total_winnings


TEST_INPUT = """\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""


def test_example1():
    assert part1(TEST_INPUT) == 6440


def test_example2():
    assert part2(TEST_INPUT) == 5905


if __name__ == "__main__":
    with open("inputs/day07.txt") as fin:
        inputs = fin.read()

    print(f"Part 1: {part1(inputs)}")
    print(f"Part 2: {part2(inputs)}")
