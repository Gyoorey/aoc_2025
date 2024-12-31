from math import inf
import numpy as np
from collections import defaultdict


def segment_region(warehouse, start_x, start_y, direction="up"):
    region = set()
    wavefront = [(start_x, start_y)]
    while wavefront:
        x, y = wavefront.pop()
        region.add((x, y))
        if warehouse[y, x] == '[':
            if (x+1, y) not in region:
                wavefront.append((x+1, y))
        if warehouse[y, x] == ']':
            if (x-1, y) not in region:
                wavefront.append((x-1, y))
        if direction == "up":
            if warehouse[y-1, x] == '[' or warehouse[y-1, x] == ']':
                if (x, y-1) not in region:
                    wavefront.append((x, y-1))
            if warehouse[y-1, x] == '#':
                return False
        elif direction == "down":
            if warehouse[y+1, x] == '[' or warehouse[y+1, x] == ']':
                if (x, y+1) not in region:
                    wavefront.append((x, y+1))
            if warehouse[y+1, x] == '#':
                return False

    if direction == "up":
        region_list = sorted(region, key=lambda pos: (pos[1], pos[0]))
        return region_list
    else:
        region_list = sorted(region, key=lambda pos: (
            pos[1], pos[0]), reverse=True)
        return region_list


def vertical_moves(warehouse, start_x, start_y, direction="up"):
    region = segment_region(warehouse, start_x, start_y, direction)
    if not region:
        return
    for x, y in region:
        if direction == "up":
            warehouse[y-1][x] = warehouse[y][x]
            warehouse[y][x] = '.'
        elif direction == "down":
            warehouse[y+1][x] = warehouse[y][x]
            warehouse[y][x] = '.'
    return True


def move_robot(slice_):
    for i, cell in enumerate(slice_):
        if cell == '.':
            slice_[1:i+1] = slice_[0:i]
            slice_[0] = '.'
            return 1
        elif cell == '#':
            return 0


def calculate_score(warehouse):
    score = 0
    for i in range(1, len(warehouse) - 1):
        for j in range(1, len(warehouse[0]) - 1):
            if warehouse[i][j] == 'O' or warehouse[i][j] == '[':
                score += 100 * i + j
    return score


def part1(warehouse, robot_positions, moves):
    current_position = robot_positions
    for move in moves:
        if move == '^':
            slice_ = warehouse[:current_position[1] +
                               1, current_position[0]][::-1]
            moved = move_robot(slice_)
            current_position = (
                current_position[0], current_position[1] - moved)
        elif move == '>':
            slice_ = warehouse[current_position[1], current_position[0]:]
            moved = move_robot(slice_)
            current_position = (
                current_position[0] + moved, current_position[1])
        elif move == 'v':
            slice_ = warehouse[current_position[1]:, current_position[0]]
            moved = move_robot(slice_)
            current_position = (
                current_position[0], current_position[1] + moved)
        elif move == '<':
            slice_ = warehouse[current_position[1],
                               :current_position[0]+1][::-1]
            moved = move_robot(slice_)
            current_position = (
                current_position[0] - moved, current_position[1])

    return calculate_score(warehouse)


def part2(warehouse_lines, moves):
    transformed_warehouse = []
    for line in warehouse_lines:
        line = line.replace('.', '..')
        line = line.replace('#', '##')
        line = line.replace('O', '[]')
        line = line.replace('@', '@.')
        transformed_warehouse.append(line)
    robot_positions = "".join(transformed_warehouse).find("@")
    robot_positions = (robot_positions % len(transformed_warehouse[0]),
                       robot_positions // len(transformed_warehouse[0]))
    warehouse = np.array([list(line) for line in transformed_warehouse])
    current_position = robot_positions
    for move in moves:
        if move == '^':
            success = vertical_moves(
                warehouse, current_position[0], current_position[1], "up")
            if success:
                current_position = (
                    current_position[0], current_position[1] - 1)
        elif move == '>':
            slice_ = warehouse[current_position[1], current_position[0]:]
            moved = move_robot(slice_)
            current_position = (
                current_position[0] + moved, current_position[1])
        elif move == 'v':
            success = vertical_moves(
                warehouse, current_position[0], current_position[1], "down")
            if success:
                current_position = (
                    current_position[0], current_position[1] + 1)
        elif move == '<':
            slice_ = warehouse[current_position[1],
                               :current_position[0]+1][::-1]
            moved = move_robot(slice_)
            current_position = (
                current_position[0] - moved, current_position[1])

    return calculate_score(warehouse)


def solve(input):
    with open(input) as file:
        lines = [line.strip() for line in file.readlines()]
        separator_index = lines.index("")
        warehouse_lines = [line for line in lines[:separator_index]]
        robot_positions = "".join(warehouse_lines).find("@")
        robot_positions = (robot_positions % len(warehouse_lines[0]),
                           robot_positions // len(warehouse_lines[0]))
        warehouse = np.array([list(line) for line in warehouse_lines])
        moves = "".join(lines[separator_index + 1:])

    return (part1(warehouse.copy(), robot_positions, moves),
            part2(warehouse_lines, moves))


if __name__ == "__main__":
    input = "input.txt"
    result = solve(input)
    print("Part 1:", result[0])
    print("Part 2:", result[1])
