
from typing import List


def reverse(lines: List[str]):

    return [line[::-1] for line in lines]


def rotate90(lines: List[str]):

    return [''.join([lines[j][i] for j in range(len(lines))]) for i in range(len(lines[0]))]


def rotate45(lines: List[str]):
    new_lines = []
    for i in range(len(lines) + len(lines[0]) - 1):
        new_line = ""
        for j in range(max(0, i - len(lines[0]) + 1), min(i + 1, len(lines))):
            new_line += lines[j][i - j]
        new_lines.append(new_line)
    return new_lines


def count_XMAS(lines: List[str]):

    return sum(line.count("XMAS") for line in lines)


def part1(input):
    with open(input) as file:
        lines = [line.strip() for line in file.readlines()]
        transformations = [lines, reverse(lines), rotate45(lines), reverse(rotate45(lines)), rotate90(
            lines), reverse(rotate90(lines)), rotate45(reverse(lines)), reverse(rotate45(reverse(lines)))]

    return sum(count_XMAS(t) for t in transformations)


def part2(input):
    with open(input) as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]
        count = 0
        patterns = [
            ("M", "M", "S", "S"),
            ("M", "S", "M", "S"),
            ("S", "M", "S", "M"),
            ("S", "S", "M", "M")
        ]
        for row in range(1, len(lines) - 1):
            for col in range(1, len(lines[0]) - 1):
                if lines[row][col] == "A":
                    for pattern in patterns:
                        if all([
                            lines[row - 1][col - 1] == pattern[0],
                            lines[row - 1][col + 1] == pattern[1],
                            lines[row + 1][col - 1] == pattern[2],
                            lines[row + 1][col + 1] == pattern[3]
                        ]):
                            count += 1
                            break

    return count


if __name__ == "__main__":
    input = "input.txt"
    print("Part 1:", part1(input))
    print("Part 2:", part2(input))
