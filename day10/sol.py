
from typing import List

target = 9
start = 0
max_inc = 1


def get_neighbors(position, N, M):
    row, col = position
    neighbors = []
    if row - 1 >= 0:
        neighbors.append((row - 1, col))
    if row + 1 < N:
        neighbors.append((row + 1, col))
    if col - 1 >= 0:
        neighbors.append((row, col - 1))
    if col + 1 < M:
        neighbors.append((row, col + 1))
    return neighbors


def find_routes(topographic_map: List[List[int]], unique=False) -> int:
    N, M = len(topographic_map), len(topographic_map[0])
    target_positions = [(row, col) for row in range(len(topographic_map)) for col in range(
        len(topographic_map[0])) if topographic_map[row][col] == target]
    score = 0
    for target_position in target_positions:
        start_positions = list()
        wavefront = list()
        wavefront.append(target_position)
        while wavefront:
            position = wavefront.pop()
            middle = topographic_map[position[0]][position[1]]
            neighbors = get_neighbors(position, N, M)
            for new_position in neighbors:
                if new_position is not None and \
                        topographic_map[new_position[0]][new_position[1]] == (middle - max_inc):
                    wavefront.append(new_position)
                    if (topographic_map[new_position[0]][new_position[1]] == start):
                        start_positions.append(new_position)
        if not unique:
            start_positions = set(start_positions)
        score += len(start_positions)

    return score


def part1(topographic_map: List[List[int]]) -> int:
    return find_routes(topographic_map)


def part2(topographic_map):
    return find_routes(topographic_map, True)


def solve(input):
    with open(input) as file:
        topographic_map = [list(map(int, line.strip()))
                           for line in file.readlines()]

    return (part1(topographic_map), part2(topographic_map))


if __name__ == "__main__":
    input = "input.txt"
    result = solve(input)
    print("Part 1:", result[0])
    print("Part 2:", result[1])
