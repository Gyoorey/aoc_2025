
import itertools
from typing import List
import re

def calculate_antinodes(antenna_pair: List[int], 
                        N: int,
                        M: int, 
                        harmonics: bool = True) -> int:
    x0, y0 = antenna_pair[0] // M, antenna_pair[0] % M
    x1, y1 = antenna_pair[1] // M, antenna_pair[1] % M
    diff_x, diff_y = x0 - x1, y0 - y1
    start_harmonics = 2 if not harmonics else 1
    max_harmonics = 2 if not harmonics else min(max(N, M), max(N, M)//max(abs(diff_x), abs(diff_y)))
    antinodes = [[x0 - i*diff_x, y0 - i*diff_y] for i in range(start_harmonics, max_harmonics+1)] + \
                [[x1 + i*diff_x, y1 + i*diff_y] for i in range(start_harmonics, max_harmonics+1)]
    
    return antinodes


def num_of_antinodes(lines: List[str], harmonics: bool = False) -> int:
    N, M = len(lines), len(lines[0])
    unique_antinodes = set()
    while match := re.search(r"[^.]", "".join(lines)):
        indecies = [x.start() for x in re.finditer(match.group(), "".join(lines))]
        antenna_pairs = list(itertools.combinations(indecies, 2))
        for antenna_pair in antenna_pairs:
            aninodes = calculate_antinodes(antenna_pair=antenna_pair, 
                                           N=N, 
                                           M=M, 
                                           harmonics=harmonics)
            for antinode in aninodes:
                if antinode[0] >= 0 and antinode[0] < N and antinode[1] >= 0 and antinode[1] < M:
                    unique_antinodes.add(tuple(antinode))

        new_lines = [line.replace(match.group(), ".") for line in lines]
        lines = new_lines

    return len(unique_antinodes)

def part1(lines: List[str]) -> int:
    return num_of_antinodes(lines)


def part2(lines: List[str]) -> int:
    return num_of_antinodes(lines, harmonics=True)

def solve(input):
    with open(input) as file:
        lines = [line.strip() for line in file.readlines()]

    return (part1(lines.copy()), part2(lines.copy()))


if __name__ == "__main__":
    input = "input.txt"
    result = solve(input)
    print("Part 1:", result[0])
    print("Part 2:", result[1])