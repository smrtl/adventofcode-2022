from pathlib import Path

LOWERCASE_A = 97
UPPERCASE_A = 65


def get_priority(letter: str) -> int:
    char = ord(letter)
    if char >= LOWERCASE_A:
        return char - LOWERCASE_A + 1
    else:
        return char - UPPERCASE_A + 27


def part1(input_file: Path) -> None:
    result = 0
    with open(input_file, 'r') as f:
        for line in f:
            half = int(len(line) / 2)
            left = set([*line[:half]])
            right = set([*line[half:]])
            dupes = left & right
            assert len(dupes) == 1  # sanity check
            result += get_priority(dupes.pop())

    print(result)


def part2(input_file: Path) -> None:
    result = 0
    index = 0
    buffer = []
    with open(input_file, 'r') as f:
        for line in f:
            buffer.append(set([*line.strip()]))
            if index % 3 == 2:
                dupes = buffer[0] & buffer[1] & buffer[2]
                assert len(dupes) == 1  # sanity check
                result += get_priority(dupes.pop())
                buffer = []
            index += 1

    print(result)


def main(input_file: Path) -> None:
    part2(input_file)
