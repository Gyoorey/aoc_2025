
from itertools import chain
from itertools import accumulate


def part1(diskmap):
    files = [i for i, count in enumerate(diskmap[::2]) for _ in range(count)]
    rlc_decoded = [i//2 if i % 2 == 0 else -1 for i, count in
                   enumerate(diskmap) for _ in range(count)]
    sum_ = sum([i*element if element >= 0 else i*files.pop()
               for i, element in enumerate(rlc_decoded[:len(files)])])

    return sum_


def part2(diskmap):
    start_poisitions = list(accumulate([0] + diskmap))
    files = [[i] * count for i, count in enumerate(diskmap[::2])]
    files_starts = start_poisitions[::2]
    holes = [count for count in map(int, diskmap[1::2])]
    hole_starts = start_poisitions[1:-1:2]
    rlc_decoded = [i//2 if i % 2 == 0 else -1 for i, count in enumerate(
        map(int, diskmap)) for _ in range(count)]
    for start, length in zip(hole_starts, holes):
        stop = False
        while not stop:
            for i in range(len(files)-1, 0, -1):
                if files_starts[i] <= start:
                    stop = True
                    break
                if len(files[i]) <= length:
                    rlc_decoded[start:start+len(files[i])] = files[i]
                    rlc_decoded[files_starts[i]:files_starts[i] +
                                len(files[i])] = [-1] * len(files[i])
                    start += len(files[i])
                    length -= len(files[i])
                    files.pop(i)
                    files_starts.pop(i)
                    break
    sum_ = sum(
        [i*element for i, element in enumerate(rlc_decoded) if element >= 0])

    return sum_


def solve(input):
    with open(input) as file:
        diskmap = file.read().strip()
        diskmap = list(map(int, diskmap))

    return (part1(diskmap), part2(diskmap))


if __name__ == "__main__":
    input = "input.txt"
    result = solve(input)
    print("Part 1:", result[0])
    print("Part 2:", result[1])
