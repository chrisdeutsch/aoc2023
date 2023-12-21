#!/usr/bin/env python
from dataclasses import dataclass
from typing import Generator


@dataclass
class Number:
    line_number: int
    span: tuple[int, int]

    def is_adjacent(self, x: int, y: int) -> bool:
        if (
            (x == self.line_number + 1 or x == self.line_number - 1)
            and self.span[0] - 1 <= y
            and y <= self.span[1]
        ):
            return True
        elif x == self.line_number and (y == self.span[0] - 1 or y == self.span[1]):
            return True

        return False


def find_numbers(lines: list[str]) -> Generator[Number, None, None]:
    for line_num, line in enumerate(lines):
        begin = None
        for char_num, char in enumerate(line):
            is_digit = char.isdigit()

            if is_digit and begin is None:
                begin = char_num
            elif not is_digit and begin is not None:
                yield Number(line_number=line_num, span=(begin, char_num))
                begin = None

        # End of line case
        if begin is not None:
            yield Number(line_number=line_num, span=(begin, len(line)))


def has_adjacent_symbol(number: Number, lines: list[str]) -> bool:
    line_num = number.line_number
    line_len = len(lines[line_num])
    begin, end = number.span

    leftmost_adjacent = max(0, begin - 1)
    rightmost_adjacent = min(line_len - 1, end)
    sl = slice(leftmost_adjacent, rightmost_adjacent + 1)

    def is_symbol(c: str) -> bool:
        return not c.isdigit() and c != "."

    # Current line
    if is_symbol(lines[line_num][leftmost_adjacent]) or is_symbol(
        lines[line_num][rightmost_adjacent]
    ):
        return True

    # Upper adjacent line
    if line_num - 1 >= 0 and any(is_symbol(c) for c in lines[line_num - 1][sl]):
        return True

    # Lower adjacent line
    if line_num + 1 < len(lines) and any(is_symbol(c) for c in lines[line_num + 1][sl]):
        return True

    return False


def part1(lines: list[str]) -> int:
    s = 0
    for number in find_numbers(lines):
        if has_adjacent_symbol(number, lines):
            sl = slice(*number.span)
            num = int(lines[number.line_number][sl])
            s += num

    return s


def find_gear_candidates(lines: list[str]) -> Generator[tuple[int, int], None, None]:
    for line_num, line in enumerate(lines):
        for char_num, char in enumerate(line):
            if char == "*":
                yield (line_num, char_num)


def part2(lines: list[str]) -> int:
    s = 0
    for gear_line_num, gear_char_num in find_gear_candidates(lines):
        num_count = 0
        num_prod = 1
        for number in find_numbers(lines):
            if not number.is_adjacent(gear_line_num, gear_char_num):
                continue

            num_count += 1
            num_prod *= int(lines[number.line_number][slice(*number.span)])

        if num_count == 2:
            s += num_prod

    return s


if __name__ == "__main__":
    with open("inputs/day03.txt") as fin:
        inputs = fin.read()

    lines = inputs.splitlines()
    print(f"Part 1: {part1(lines)}")
    print(f"Part 2: {part2(lines)}")
