from functools import cached_property


class Grid:
    def __init__(self, grid_str):
        self.rows = grid_str.splitlines()
        self.num_rows = len(self.rows)
        self.num_columns = len(self.rows[0])
        assert all(self.num_columns == len(g) for g in self.rows)

    @cached_property
    def columns(self):
        cols = []

        for i in range(self.num_columns):
            col = ""
            for j in range(self.num_rows):
                col += self.rows[j][i]

            cols.append(col)

        return cols

    def __str__(self):
        return "\n".join(self.rows)


def find_reflection(x):
    assert len(x) > 1

    for i, (first, second) in enumerate(zip(x, x[1:])):
        if first != second:
            continue

        left_idx = i - 1
        right_idx = i + 2
        while left_idx >= 0 and right_idx < len(x):
            if x[left_idx] != x[right_idx]:
                break

            left_idx -= 1
            right_idx += 1
        else:
            return i

    return None


def parse(inputs):
    for grid_str in inputs.split("\n\n"):
        yield Grid(grid_str)


def part1(inputs):
    total = 0
    for grid in parse(inputs):
        horizontal = find_reflection(grid.rows)
        vertical = find_reflection(grid.columns)

        if horizontal is not None and vertical is not None:
            raise RuntimeError("Both horizontal and vertical reflection axis possible")

        if horizontal is not None:
            total += 100 * (horizontal + 1)
        elif vertical is not None:
            total += vertical + 1
        else:
            print(grid)
            raise RuntimeError("No symmetry")

    return total


def test_cols():
    grid = Grid(".#\n..")
    print(grid)
    assert grid.columns == ["..", "#."]


TEST_INPUT = """\
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""


def test_find_reflection_vertical():
    grid = next(parse(TEST_INPUT))
    assert find_reflection(grid.columns) == 4


def test_find_reflection_horizontal_none():
    grid = next(parse(TEST_INPUT))
    assert find_reflection(grid.rows) == None


def test_find_reflection_horizontal():
    inputs = parse(TEST_INPUT)
    next(inputs)  # Discard first element
    grid = next(inputs)
    assert find_reflection(grid.rows) == 3


def test_find_reflection_vertical_none():
    inputs = parse(TEST_INPUT)
    next(inputs)  # Discard first element
    grid = next(inputs)
    assert find_reflection(grid.columns) == None


TEST_INPUT_2 = """\
...#.#.#.####.#.#
..###..###..###..
##.###..........#
....####...#..###
...#.#...#..#...#
##...##.##..##.##
###..##.#....#.##
..##.##...##...##
##.##............"""


def test_find_reflection_vertical_corner():
    grid = next(parse(TEST_INPUT_2))
    assert find_reflection(grid.columns) == 0


def test_part1():
    assert part1(TEST_INPUT) == 405


if __name__ == "__main__":
    with open("inputs/day13.txt") as fin:
        inputs = fin.read()

    print(f"Part 1: {part1(inputs)}")
