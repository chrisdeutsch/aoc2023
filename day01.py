#!/usr/bin/env python
def part1(inputs: str) -> int:
    s = 0
    for line in inputs.splitlines():
        digits = [char for char in line if char.isdigit()]
        s += int(digits[0] + digits[-1])

    return s


def part2(inputs: str) -> int:
    mapping = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }

    for num in range(1, 10):
        mapping[str(num)] = str(num)

    s = 0
    for line in inputs.splitlines():
        forward_iter = ((line.find(key), mapping[key]) for key in mapping)
        backward_iter = ((line.rfind(key), mapping[key]) for key in mapping)

        _, leftmost = min(filter(lambda x: x[0] >= 0, forward_iter))
        _, rightmost = max(filter(lambda x: x[0] >= 0, backward_iter))

        s += int(leftmost + rightmost)

    return s


if __name__ == "__main__":
    with open("inputs/day1.txt") as fin:
        inputs = fin.read()

    print(f"Part 1: {part1(inputs)}")
    print(f"Part 2: {part2(inputs)}")
