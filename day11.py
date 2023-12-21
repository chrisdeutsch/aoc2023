#!/usr/bin/env python
from itertools import combinations


def parse(inputs: str) -> list[list[str]]:
    return list(map(lambda x: list(x), inputs.splitlines()))


def expand(galaxy: list[list[str]]) -> list[list[str]]:
    num_rows = len(galaxy)
    num_cols = len(galaxy[0])

    expand_row = []
    for rownum in range(num_rows):
        expand_row.append(all(galaxy[rownum][i] == "." for i in range(num_cols)))

    expand_col = []
    for colnum in range(num_cols):
        expand_col.append(all(galaxy[i][colnum] == "." for i in range(num_rows)))

    # Expand rows
    while any(expand_row):
        idx = expand_row.index(True)

        galaxy.insert(idx, ["."] * num_cols)

        expand_row[idx] = False
        expand_row.insert(0, False)
        num_rows += 1

    # Expand cols
    while any(expand_col):
        idx = expand_col.index(True)

        for rownum in range(num_rows):
            galaxy[rownum].insert(idx, ".")

        expand_col[idx] = False
        expand_col.insert(0, False)
        num_cols += 1

    return galaxy


def get_expansion_factors(
    galaxy: list[list[str]], factor: int = 2
) -> tuple[list[int], list[int]]:
    num_rows = len(galaxy)
    num_cols = len(galaxy[0])

    row_expansion_factors = []
    for rownum in range(num_rows):
        if all(galaxy[rownum][i] == "." for i in range(num_cols)):
            row_expansion_factors.append(factor)
        else:
            row_expansion_factors.append(1)

    col_expansion_factors = []
    for colnum in range(num_cols):
        if all(galaxy[i][colnum] == "." for i in range(num_rows)):
            col_expansion_factors.append(factor)
        else:
            col_expansion_factors.append(1)

    return row_expansion_factors, col_expansion_factors


def get_galaxy_coords(galaxy: list[list[str]]) -> list[tuple[int, int]]:
    galaxies = []
    for rownum, row in enumerate(galaxy):
        gen = (colnum for colnum, c in enumerate(row) if c == "#")
        for colnum in gen:
            galaxies.append((rownum, colnum))

    return galaxies


def part1(inputs: str) -> int:
    galaxy = expand(parse(inputs))
    coords = get_galaxy_coords(galaxy)

    total_distance = 0
    for (x1, y1), (x2, y2) in combinations(coords, 2):
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)
        total_distance += dx + dy

    return total_distance


def part2(inputs: str, factor: int = 1000000) -> int:
    galaxy = parse(inputs)
    coords = get_galaxy_coords(galaxy)
    row_facts, col_facts = get_expansion_factors(galaxy, factor=factor)

    total_distance = 0
    for (x1, y1), (x2, y2) in combinations(coords, 2):
        dx = 0
        for i in range(min(x1, x2), max(x1, x2)):
            dx += row_facts[i]

        dy = 0
        for i in range(min(y1, y2), max(y1, y2)):
            dy += col_facts[i]

        total_distance += dx + dy

    return total_distance


TEST_INPUT = """\
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""

TEST_INPUT_EXPANDED = """\
....#........
.........#...
#............
.............
.............
........#....
.#...........
............#
.............
.............
.........#...
#....#......."""


def test_expand() -> None:
    galaxy = parse(TEST_INPUT)
    galaxy_expanded = parse(TEST_INPUT_EXPANDED)
    assert expand(galaxy) == galaxy_expanded


def test_get_galaxy_coords() -> None:
    test = """\
.#..
..#.
...#"""
    assert get_galaxy_coords(parse(test)) == [(0, 1), (1, 2), (2, 3)]


def test_part1() -> None:
    assert part1(TEST_INPUT) == 374


def test_part1_smarter() -> None:
    assert part2(TEST_INPUT, factor=2) == 374


if __name__ == "__main__":
    with open("inputs/day11.txt") as fin:
        inputs = fin.read()

    print(f"Part 1: {part1(inputs)}")
    print(f"Part 2: {part2(inputs)}")
