import itertools
import numpy as np

def get_neighbors(row, col, max_distance):
    neighbors = []
    for dr in range(-max_distance, max_distance + 1):
        for dc in range(-max_distance, max_distance + 1):
            if abs(dr) + abs(dc) <= max_distance:
                neighbors.append((row + dr, col + dc, abs(dr) + abs(dc)))
    return neighbors

def find_cheats(map_: np.array, max_distance=2, min_cheat=100):
    start_row, start_col = np.where(map_ == "S")
    end_row, end_col = np.where(map_ == "E")
    map_[start_row, start_col] = "."
    map_[end_row, end_col] = "."
    # find costs
    costs = {(start_row[0], start_col[0]): 0}
    queue = [(start_row, start_col)]
    while queue:
        row, col = queue.pop(0)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < map_.shape[0] and 0 <= new_col < map_.shape[1]:
                if (new_row[0], new_col[0]) not in costs and map_[new_row, new_col] == ".":
                    costs[(new_row[0], new_col[0])] = costs[(row[0], col[0])] + 1
                    queue.append((new_row, new_col))
    # find cheats
    num_of_cheats = 0
    for (row, col) in costs:
        start_cost = costs[(row, col)]
        neighbors = get_neighbors(row, col, max_distance=max_distance)
        for row2, col2, dist in neighbors:
            target_cost = costs.get((row2, col2), None)
            if target_cost is not None and target_cost > start_cost:
                if target_cost - start_cost - dist >= min_cheat:
                    num_of_cheats += 1
    
    return num_of_cheats

def part1(map_: np.array):
    return find_cheats(map_)

def part2(map_: np.array):
    return find_cheats(map_, max_distance=20)

def solve(input):
    with open(input) as file:
        lines = [line.strip() for line in file.readlines()]
        map_: np.array = np.array([[c for c in line] for line in lines])

    map_copy = np.copy(map_)
    return (part1(map_copy), part2(map_))


if __name__ == "__main__":
    input = "input.txt"
    result = solve(input)
    print("Part 1:", result[0])
    print("Part 2:", result[1])