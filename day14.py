from copy import deepcopy


def parse(inputs):
    return list(map(list, inputs.splitlines()))


def tilt_north(grid):
    grid = deepcopy(grid)
    num_rows = len(grid)
    num_columns = len(grid[0])

    for col in range(num_columns):
        placement_row = 0
        for row in range(num_rows):
            char = grid[row][col]

            if char == "#":
                placement_row = row + 1
            elif char == "O":
                grid[row][col] = "."
                grid[placement_row][col] = "O"
                placement_row += 1
            else:
                pass

    return grid


def get_load(rows):
    total_load = 0
    for load_per_rock, row in enumerate(reversed(rows), 1):
        total_load += sum(load_per_rock for char in row if char == "O")
    return total_load


def part1(inputs):
    grid = parse(inputs)
    grid_tilted = tilt_north(grid)
    return get_load(grid_tilted)

TEST_INPUT = """\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""


TEST_INPUT_2 = """\
OOOO.#.O..
OO..#....#
OO..O##..O
O..#.OO...
........#.
..#....#.#
..O..#.O.O
..O.......
#....###..
#....#...."""


def test_parse():
    assert parse("O.\n.#\n..") == [["O", "."], [".", "#"], [".", "."]]


def test_tilt_north():
    grid = tilt_north(parse(TEST_INPUT))
    assert "\n".join(map(lambda x: "".join(x), grid)) == TEST_INPUT_2


def test_load():
    assert get_load(parse(TEST_INPUT_2)) == 136


def test_part1():
    assert part1(TEST_INPUT) == 136


if __name__ == "__main__":
    with open("inputs/day14.txt") as fin:
        inputs = fin.read()

    print(f"Part 1: {part1(inputs)}")