#!/usr/bin/env python
import pytest
from functools import cache


def parse(inputs):
    for line in inputs.splitlines():
        record, runs = line.split()
        yield record, [int(x) for x in runs.split(",")]


def count_arrangements(record, runs):
    @cache
    def f(idx, run_idx, current_run_len):
        # Termination condition
        if idx == len(record):
            if run_idx == len(runs) and current_run_len == 0:
                return 1
            elif run_idx == len(runs) - 1 and current_run_len == runs[run_idx]:
                return 1
            else:
                return 0

        # Recurse
        arrangements = 0

        if record[idx] == "#" or record[idx] == "?":
            if run_idx < len(runs) and current_run_len < runs[run_idx]:
                # Advance & extend run if it matches requirement
                arrangements += f(idx + 1, run_idx, current_run_len + 1)

        if record[idx] == "." or record[idx] == "?":
            if current_run_len == 0:
                # Simply advance if not currently in a block
                arrangements += f(idx + 1, run_idx, 0)
            elif current_run_len == runs[run_idx]:
                # Advance & advance block only if it matches requirement
                arrangements += f(idx + 1, run_idx + 1, 0)

        return arrangements

    return f(0, 0, 0)


def part1(inputs):
    total = 0
    for record, runs in parse(inputs):
        total += count_arrangements(record, runs)

    return total


def part2(inputs):
    total = 0
    for i, (record, runs) in enumerate(parse(inputs)):
        total += count_arrangements("?".join(5 * [record]), 5 * runs)

    return total


TEST_INPUTS = [
    ("#.#.### 1,1,3", 1),
    ("???.### 1,1,3", 1),
    (".??..??...?##. 1,1,3", 4),
    ("?#?#?#?#?#?#?#? 1,3,1,6", 1),
    ("????.#...#... 4,1,1", 1),
    ("????.######..#####. 1,6,5", 4),
    ("?###???????? 3,2,1", 10),
]


@pytest.mark.parametrize("inputs, expected", TEST_INPUTS)
def test_count_arrangements(inputs, expected):
    record, runs = next(parse(inputs))
    assert count_arrangements(record, runs) == expected


TEST_INPUTS_PT2 = [
    ("???.### 1,1,3", 1),
    (".??..??...?##. 1,1,3", 16384),
    ("?#?#?#?#?#?#?#? 1,3,1,6", 1),
    ("????.#...#... 4,1,1", 16),
    ("????.######..#####. 1,6,5", 2500),
    ("?###???????? 3,2,1", 506250),
]


@pytest.mark.parametrize("inputs, expected", TEST_INPUTS_PT2)
def test_count_arrangements_pt2(inputs, expected):
    record, runs = next(parse(inputs))
    assert count_arrangements("?".join(5 * [record]), 5 * runs) == expected


if __name__ == "__main__":
    with open("inputs/day12.txt") as fin:
        inputs = fin.read()

    print(f"Part 1: {part1(inputs)}")
    print(f"Part 2: {part2(inputs)}")
