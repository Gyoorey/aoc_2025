import os


def check_value(value: int) -> bool:
    value_str = str(value)
    return value_str[:len(value_str) // 2] == value_str[len(value_str) // 2:]


def check_value_all_substrings(value: int) -> bool:
    value_str = str(value)
    length = len(value_str)
    for size in range(1, length // 2 + 1):
        if length % size != 0:
            continue
        substrings = [value_str[i:i + size]
                      for i in range(0, length, size)]
        if all(s == substrings[0] for s in substrings):
            return True

    return False


def check_range(range_: list[int]) -> tuple[int, int]:
    sum_of_invalid = 0
    sum_of_invalid_pt2 = 0
    for i in range(range_[0], range_[1] + 1):
        if check_value(i):
            sum_of_invalid += i
        if check_value_all_substrings(i):
            sum_of_invalid_pt2 += i
    return sum_of_invalid, sum_of_invalid_pt2


def solve(input_path: str) -> None:
    with open(input_path, "r") as file:
        line = file.readline().strip()
        ranges = line.split(",")
        ranges = [[int(s), int(e)] for r in ranges for s, e in [r.split("-")]]
        sum_of_invalid = 0
        sum_of_invalid_pt2 = 0
        for range_ in ranges:
            result = check_range(range_)
            sum_of_invalid += result[0]
            sum_of_invalid_pt2 += result[1]
    print(f"Total sum of invalid values: {sum_of_invalid}")
    print(f"Total sum of invalid values (part 2): {sum_of_invalid_pt2}")


if __name__ == "__main__":
    input_path = os.path.join("inputs", "2", "input.txt")
    solve(input_path)
