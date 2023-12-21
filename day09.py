#!/usr/bin/env python
import pytest


def parse(inputs: str) -> list[list[int]]:
    histories = []
    for line in inputs.splitlines():
        mapped_to_int = map(int, line.split())
        histories.append(list(mapped_to_int))

    return histories


def forecast(history: list[int], backwards: bool=False) -> int:
    steps = [history]

    while not all(element == 0 for element in history):
        history = [y - x for x, y in zip(history, history[1:])]
        steps.append(history)

    if backwards:
        last = 0
        for history in reversed(steps[:-1]):
            last = history[0] - last

        return last
    else:
        total = 0
        for history in reversed(steps[:-1]):
            total += history[-1]

        return total


def part1(inputs: str) -> int:
    histories = parse(inputs)

    total = 0
    for history in histories:
        total += forecast(history)

    return total


def part2(inputs: str) -> int:
    histories = parse(inputs)

    total = 0
    for history in histories:
        total += forecast(history, backwards=True)

    return total


TEST_1 = "0 3 6 9 12 15"
TEST_2 = "1 3 6 10 15 21"
TEST_3 = "10 13 16 21 30 45"


@pytest.mark.parametrize(
    "inputs,expected",
    [(TEST_1, 18), (TEST_2, 28), (TEST_3, 68)],
    ids=["case1", "case2", "case3"],
)
def test_forecast(inputs: str, expected: int) -> None:
    (history,) = parse(inputs)
    assert forecast(history) == expected


def test_part1() -> None:
    inputs = "\n".join([TEST_1, TEST_2, TEST_3])
    assert part1(inputs) == 114


@pytest.mark.parametrize(
    "inputs,expected",
    [(TEST_1, -3), (TEST_2, 0), (TEST_3, 5)],
    ids=["case1", "case2", "case3"],
)
def test_backcast(inputs: str, expected: int) -> None:
    (history,) = parse(inputs)
    assert forecast(history, backwards=True) == expected


def test_part2() -> None:
    inputs = "\n".join([TEST_1, TEST_2, TEST_3])
    assert part2(inputs) == 2


if __name__ == "__main__":
    with open("inputs/day09.txt") as fin:
        inputs = fin.read()

    print(f"Part 1: {part1(inputs)}")
    print(f"Part 2: {part2(inputs)}")
