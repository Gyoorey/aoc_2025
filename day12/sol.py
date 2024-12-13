from collections import defaultdict
from typing import List

directions = ['_', '^', '|l', 'r|']


def get_sides(sides):
    num_of_sides = 0
    for direction in directions:
        edges = sides[direction]
        # find horizontal edges
        if direction in ['^', '_']:
            rows = set([edge[0] for edge in edges])
            for row in rows:
                cols = sorted([edge[1] for edge in edges if edge[0] == row])
                num_of_sides += 1 + \
                    sum(1 for j in range(1, len(cols))
                        if cols[j] - cols[j-1] != 1)

        # find vertical edges
        else:
            cols = set([pos[1] for pos in edges])
            for col in cols:
                rows = sorted([pos[0] for pos in edges if pos[1] == col])
                num_of_sides += 1 + \
                    sum(1 for j in range(1, len(rows))
                        if rows[j] - rows[j-1] != 1)

    return num_of_sides


def store_outer_sides(position, sides, N, M):
    if position[0] == 0:
        sides['^'].append(position)
    if position[0] == N - 1:
        sides['_'].append(position)
    if position[1] == 0:
        sides['|l'].append(position)
    if position[1] == M - 1:
        sides['r|'].append(position)


def get_neighbors(position, N, M):
    row, col = position
    neighbors = []
    if row - 1 >= 0:
        neighbors.append((row - 1, col, '^'))
    if row + 1 < N:
        neighbors.append((row + 1, col, '_'))
    if col - 1 >= 0:
        neighbors.append((row, col - 1, '|l'))
    if col + 1 < M:
        neighbors.append((row, col + 1, 'r|'))
    return neighbors


def get_cost(lines: List[str], use_sides=False) -> int:
    N, M = len(lines), len(lines[0])
    cost = 0
    for row in range(N):
        for col in range(M):
            if lines[row][col] == '.':
                continue
            area, perimeter = 0, 0
            sides = defaultdict(list)
            wavefront = [(row, col)]
            region = set()
            while wavefront:
                position = wavefront.pop()
                if position in region:
                    continue
                region.add(position)
                area += 1
                neighbors = get_neighbors(position, N, M)
                perimeter += 4 - len(neighbors)
                store_outer_sides(position, sides, N, M)
                for new_position in neighbors:
                    if lines[new_position[0]][new_position[1]] == lines[row][col]:
                        if new_position[:2] not in region:
                            wavefront.append(new_position[:2])
                    else:
                        sides[new_position[2]].append(position)
                        perimeter += 1

            cost += area * (get_sides(sides) if use_sides else perimeter)
            for position in region:
                lines[position[0]] = lines[position[0]][:position[1]] + \
                    '.' + lines[position[0]][position[1] + 1:]

    return cost


def part1(lines: List[str]) -> int:
    return get_cost(lines)


def part2(lines: List[str]) -> int:
    return get_cost(lines, use_sides=True)


def solve(input):
    with open(input) as file:
        lines = [line.strip() for line in file.readlines()]

    return (part1(lines.copy()), part2(lines.copy()))


if __name__ == "__main__":
    input = "input.txt"
    result = solve(input)
    print("Part 1:", result[0])
    print("Part 2:", result[1])
