import os


def solve(input_path: str) -> None:
    left_zero: int = 0
    hit_zero: int = 0
    lock_state: int = 50
    with open(input_path, "r") as file:
        for line in file:
            line = line.strip()
            direction, rotation = line[0], int(line[1:])
            prev_state = lock_state
            hit_zero += rotation // 100
            rotation %= 100

            if direction == "L":
                lock_state -= rotation
            else:
                lock_state += rotation

            if (lock_state <= 0 and prev_state > 0) or lock_state > 99:
                hit_zero += 1
            lock_state %= 100

            if prev_state == 0 and lock_state != 0:
                left_zero += 1

    print(f"Left zero count: {left_zero}")
    print(f"Hit zero count: {hit_zero}")


if __name__ == "__main__":
    input_path = os.path.join("inputs", "1", "input.txt")
    solve(input_path)
