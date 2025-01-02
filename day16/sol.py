from collections import defaultdict
from math import inf
import numpy as np
from enum import Enum


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


def find_paths(map_, start_position, end_position):
    dir_names = {
        Direction.NORTH: [Direction.EAST, Direction.WEST, Direction.NORTH],
        Direction.EAST: [Direction.NORTH, Direction.SOUTH, Direction.EAST],
        Direction.SOUTH: [Direction.EAST, Direction.WEST, Direction.SOUTH],
        Direction.WEST: [Direction.NORTH, Direction.SOUTH, Direction.WEST]
    }
    directions = {
        Direction.NORTH: [(1, 0), (-1, 0), (0, -1)],
        Direction.EAST: [(0, -1), (0, 1), (1, 0)],
        Direction.SOUTH: [(1, 0), (-1, 0), (0, 1)],
        Direction.WEST: [(0, -1), (0, 1), (-1, 0)]
    }
    min_costs = defaultdict(lambda: defaultdict(lambda: inf))
    wavefront = [(start_position[1],
                  start_position[0],
                  Direction.EAST,
                  0)]
    while wavefront:
        x, y, dir, cost = wavefront.pop(0)
        if (y, x) == end_position:
            continue
        for (dx, dy), dir_name in zip(directions[dir], dir_names[dir]):
            nx, ny = x + dx, y + dy
            if map_[ny, nx] == '#':
                continue
            same_dir = (dir_name == dir)
            new_cost = cost + (1 if same_dir else 1001)
            if new_cost >= min_costs[(ny, nx)][dir_name]:
                continue
            wavefront.append((nx, ny, dir_name, new_cost))
            min_costs[(ny, nx)][dir_name] = new_cost
    min_cost = min(min_costs[(end_position[0], end_position[1])].values())

    return min_cost, min_costs


def part1(map_: np.array):
    return find_paths(map_, (map_.shape[0] - 2, 1), (1, map_.shape[1] - 2))


def part2(min_costs, start_position, end_position, map_):
    to_direction = {
        Direction.NORTH: (0, 1),
        Direction.EAST: (-1, 0),
        Direction.SOUTH: (0, -1),
        Direction.WEST: (1, 0)
    }
    min_cost, min_direction = min(
        (min_costs[(end_position[0], end_position[1])][direction], direction)
        for direction in Direction
    )
    seats = set()
    seats.add(end_position)
    seats.add(start_position)
    wavefront = [(end_position[1], end_position[0], min_cost, min_direction)]
    while wavefront:
        x, y, cost, dir = wavefront.pop(0)
        seats.add((y, x))
        if (y, x) == start_position:
            continue
        parent = (y + to_direction[dir][1], x + to_direction[dir][0])
        parent_dirs, parent_costs = (min_costs[parent].keys(),
                                     min_costs[parent].values())
        for pc, pd in zip(parent_costs, parent_dirs):
            if pc == cost - 1 or pc == cost - 1001:
                wavefront.append((parent[1], parent[0], pc, pd))

    return len(seats)


def solve(input):
    with open(input) as file:
        lines = [line.strip() for line in file.readlines()]
        map_ = np.array([[c for c in line] for line in lines])

    part1_sol, paths = part1(map_.copy())

    return (part1_sol, part2(paths, (map_.shape[0] - 2, 1), (1, map_.shape[1] - 2), map_=map_.copy()))


if __name__ == "__main__":
    input = "input.txt"
    result = solve(input)
    print("Part 1:", result[0])
    print("Part 2:", result[1])
