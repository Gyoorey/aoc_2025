import os
import numpy as np


def get_neighbors(r: int, c: int, num_rows: int, num_cols: int) -> list[tuple[int, int]]:
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < num_rows and 0 <= nc < num_cols:
                neighbors.append((nr, nc))
    return neighbors


def solve_part1(table: np.ndarray) -> tuple[int, np.ndarray, int]:
    num_rows, num_cols = table.shape
    count = 0
    hit_map = np.zeros((num_rows, num_cols), dtype=bool)
    for r in range(num_rows):
        for c in range(num_cols):
            if table[r, c] != '@':
                continue
            neighbors = get_neighbors(r, c, num_rows, num_cols)
            neighbor_cells = [table[nr, nc] for nr, nc in neighbors]
            count_rolls = neighbor_cells.count('@')
            if count_rolls < 4:
                count += 1
                hit_map[r, c] = True

    table[hit_map] = '.'

    return count, table, hit_map.sum()


def solve_part2(table: np.ndarray) -> int:
    total_count = 0
    count, table, changed = solve_part1(table)
    total_count += count
    while changed > 0:
        count, table, changed = solve_part1(table)
        total_count += count

    return total_count


def solve(input_path: str) -> None:
    rows = []
    with open(input_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            row = [i for i in line.strip()]
            rows.append(row)
    table_array = np.array(rows)
    part1, _, _ = solve_part1(table_array)
    print(f"Part 1: {part1}")

    table_array = np.array(rows)
    part2 = solve_part2(table_array)
    print(f"Part 2: {part2}")


if __name__ == "__main__":
    input_path = os.path.join("inputs", "4", "input.txt")
    solve(input_path)
