#!/usr/bin/env python
from itertools import combinations


def parse(inputs):
    return list(map(list, inputs.splitlines()))


def expand(galaxy):
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


def get_galaxy_coords(galaxy):
    galaxies = []
    for rownum, row in enumerate(galaxy):
        gen = (colnum for colnum, c in enumerate(row) if c == "#")
        for colnum in gen:
            galaxies.append((rownum, colnum))

    return galaxies


def part1(inputs):
    galaxy = expand(parse(inputs))
    coords = get_galaxy_coords(galaxy)

    total_distance = 0
    for (x1, y1), (x2, y2) in combinations(coords, 2):
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)
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


def test_expand():
    galaxy = parse(TEST_INPUT)
    galaxy_expanded = parse(TEST_INPUT_EXPANDED)
    assert expand(galaxy) == galaxy_expanded


def test_get_galaxy_coords():
    test = """\
.#..
..#.
...#"""
    assert get_galaxy_coords(parse(test)) == [(0, 1), (1, 2), (2, 3)]


def test_part1():
    assert part1(TEST_INPUT) == 374


if __name__ == "__main__":
    with open("inputs/day11.txt") as fin:
        inputs = fin.read()

    print(f"Part 1: {part1(inputs)}")
