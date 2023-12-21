import pytest


def parse(inputs: str) -> list[str]:
    return [split.strip() for split in inputs.split(",")]


def aoc_hash(string: str) -> int:
    val = 0
    for char in string:
        val += ord(char)
        val *= 17
        val %= 256

    return val


def part1(inputs: str) -> int:
    sum = 0
    for init_seq in parse(inputs):
        if init_seq == "\n":
            print("BLAA")
        sum += aoc_hash(init_seq)
    return sum


@pytest.mark.parametrize(
    "string, expected",
    [
        ("HASH", 52),
        ("rn=1", 30),
        ("cm-", 253),
        ("qp=3", 97),
        ("pc-", 48),
    ],
)
def test_hash(string: str, expected: int) -> None:
    assert aoc_hash(string) == expected


def test_part1() -> None:
    test_input = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"
    assert part1(test_input) == 1320


if __name__ == "__main__":
    with open("inputs/day15.txt") as fin:
        inputs = fin.read()

    print(f"Part 1: {part1(inputs)}")
