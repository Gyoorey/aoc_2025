import os


def solve_part1(banks: list[list[int]]) -> int:
    total = 0
    for bank in banks:
        max_index = bank.index(max(bank[:-1]))
        residual = bank[max_index+1:]
        next_max = residual.index(max(residual)) + max_index + 1
        total += 10*bank[max_index] + bank[next_max]

    return total


def solve_part2(banks: list[list[int]]) -> int:
    total = 0
    for bank in banks:
        battery_needed = 12
        selected_inedices = []
        while battery_needed > 0:
            start_index = 0 if not selected_inedices else selected_inedices[-1] + 1
            if battery_needed == 1:
                max_index = bank.index(max(bank[start_index:]))
                selected_inedices.append(max_index)
                break
            part = bank[start_index:-battery_needed+1]
            max_index = part.index(max(part)) + start_index
            selected_inedices.append(max_index)
            battery_needed -= 1

        bank_values_str = ''.join(str(bank[i]) for i in selected_inedices)
        total += int(bank_values_str)

    return total


def solve(input_path: str) -> None:
    with open(input_path, "r") as file:
        battery_banks = []
        for line in file:
            bank = [int(x) for x in line.strip()]
            battery_banks.append(bank)

    result_part1 = solve_part1(battery_banks)
    print(f"Part 1: {result_part1}")

    result_part2 = solve_part2(battery_banks)
    print(f"Part 2: {result_part2}")


if __name__ == "__main__":
    input_path = os.path.join("inputs", "3", "input.txt")
    solve(input_path)
