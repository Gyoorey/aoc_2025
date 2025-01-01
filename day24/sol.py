from collections import defaultdict
from matplotlib import pyplot as plt
import random
from itertools import product


def solve_system(init_states, eqs):
    known_variables = set(init_states.keys())
    equations = []
    for eq in eqs:
        parts = eq.split(" ")
        lhs, op, rhs, _, res = parts
        equation = [lhs, rhs, op, res]
        equations.append(equation)
    solved_equations = []
    while equations:
        no_progress = True
        for eq in equations[:]:
            lhs, rhs, op, res = eq
            if lhs in known_variables and rhs in known_variables:
                if op == "AND":
                    init_states[res] = init_states[lhs] & init_states[rhs]
                elif op == "OR":
                    init_states[res] = init_states[lhs] | init_states[rhs]
                elif op == "XOR":
                    init_states[res] = init_states[lhs] ^ init_states[rhs]
                solved_equations.append(eq)
                equations.remove(eq)
                known_variables.add(res)
                no_progress = False
        if no_progress:
            return None
        if not solved_equations:
            break
    output = {k: v for k, v in sorted(init_states.items()) if k.startswith('z')}
    binary_string = ''.join(['1' if init_states[k] else '0' 
                             for k in sorted(output.keys(), reverse=True)])
    return int(binary_string, 2)


def generate_integer(n_bits = 45):
    random_bits = [random.choice([0, 1]) for _ in range(n_bits)]
    binary_string = ''.join(map(str, random_bits))
    return int(binary_string, 2)


def to_binary_string(integer, n_bits = 45):
    binary_string = bin(integer)[2:]
    return "0"*(n_bits-len(binary_string)) + binary_string


def to_variables(binary_string, prefix):
    return {f"{prefix}{i:02d}": True if bit=='1' else False 
            for i, bit in enumerate(binary_string[::-1])}


def get_outputs_for_bit(bit, prefix, eqs):
    related_outputs = set()
    symbols = [f"{prefix}{bit:02d}"]
    while symbols:
        symbol = symbols.pop()
        related_outputs.add(symbol)
        for eq in eqs:
            if symbol == eq[3]:
                symbols.append(eq[0])
                symbols.append(eq[1])
    return related_outputs


# best pattern to test addition and carry propagation
def get_error_bits_simple(eqs):
    x_values = [1 << i for i in range(45)]
    y_values = [1 << i for i in range(45)]
    z_values = [x_values[i] + y_values[i] for i in range(45)]
    error_histogram = defaultdict(int)
    for x,y,z in zip(x_values, y_values, z_values):
        init_states = to_variables(to_binary_string(x), "x")
        init_states.update(to_variables(to_binary_string(y), "y"))
        result = solve_system(init_states, eqs)
        if result is None:
            return None, None
        result = to_binary_string(result, 46)
        expected = to_binary_string(z, 46)
        for i, (r, e) in enumerate(zip(result[::-1], expected[::-1])):
            if r != e:
                error_histogram[i] += 1
    error_bits = [k for k, v in error_histogram.items() if v > 0]

    return error_bits, error_histogram


# test full addition and carry propagation
def get_error_bits_full(eqs):
    random.seed(42)
    num_of_tests = 1000
    x_values = [generate_integer() for _ in range(num_of_tests)]
    y_values = [generate_integer() for _ in range(num_of_tests)]
    z_values = [x_values[i] + y_values[i] for i in range(num_of_tests)]
    error_histogram = defaultdict(int)
    for x,y,z in zip(x_values, y_values, z_values):
        init_states = to_variables(to_binary_string(x), "x")
        init_states.update(to_variables(to_binary_string(y), "y"))
        result = solve_system(init_states, eqs)
        if result is None:
            break
        result = to_binary_string(result, 46)
        expected = to_binary_string(z, 46)
        for i, (r, e) in enumerate(zip(result[::-1], expected[::-1])):
            if r != e:
                error_histogram[i] += 1
    error_bits = [k for k, v in error_histogram.items() if v > 0]

    return error_bits, error_histogram


def swap_outputs(eqs, combination):
    equations_ = eqs.copy()
    ret = []
    for eq in equations_:
        eq = eq[:-4] + eq[-4:].replace(combination[0], "XXX")
        eq = eq[:-4] + eq[-4:].replace(combination[1], combination[0])
        eq = eq[:-4] + eq[-4:].replace("XXX", combination[1])
        ret.append(eq)
    return ret

def part1(init_states, eqs):
    init_states = {name: True if int(value)==1 else False for name, value 
                   in [state.split(": ") for state in init_states]}
    result = solve_system(init_states, eqs)

    return result


def part2(eqs):
    # first, try to find faulty bit pairs
    error_bits, error_histogram = get_error_bits_simple(eqs)
    plt.bar(error_histogram.keys(), error_histogram.values())
    plt.xlabel("Bit position")
    plt.ylabel("Number of errors")
    plt.title("Error histogram")
    plt.savefig('faulty_bits.png')
    plt.close()
    # from the figure it can be seen that faults are in pairs
    bit_pairs = [(error_bits[i], error_bits[i+1]) 
                 for i in range(0, len(error_bits), 2)]
    # translate equations to better format
    equations = []
    for eq in eqs:
        lhs, op, rhs, _, res = eq.split(" ")
        equation = [lhs, rhs, op, res]
        equations.append(equation)
    # for each faulty bit pair, find such swaps that get rid of 
    # the corresponding error bits
    filtered_combinations = defaultdict(list)
    for b, bit_pair in enumerate(bit_pairs):
        # find outputs related to the faulty bits
        related_outputs = set()
        for bit in bit_pair:
            related_outputs = related_outputs.union(get_outputs_for_bit(bit, "z", equations))
        eq_outputs = set([eq[3] for eq in equations])
        # these are the suspicious outputs
        eq_outputs = eq_outputs.intersection(related_outputs)
        swaps = [(a, b) 
                        for i, a in enumerate(eq_outputs) 
                        for j, b in enumerate(eq_outputs) if i < j]
        for swap in swaps:
            # do the swap and test the error bits
            equations_ = swap_outputs(eqs, swap)
            error_bits_, error_histogram = get_error_bits_simple(equations_)
            if error_bits_ is None:
                continue
            # this is one possible fix
            if bit_pair[0] not in error_bits_ and bit_pair[1] not in error_bits_:
                filtered_combinations[b].append(swap)
    # try to fix all errors
    four_combinations = list(product(*filtered_combinations.values()))
    for swap in four_combinations:
        equations_ = eqs.copy()
        # do all swaps
        for c in swap:
            equations_ = swap_outputs(equations_, c)
        # test with full addition
        error_bits_, error_histogram = get_error_bits_full(equations_)
        # if no errors, we are done
        if sum(error_histogram.values()) == 0:
            sorted_combination = sorted([item for sublist in swap for item in sublist])
            sorted_combination = ','.join(sorted_combination)
            break

    return sorted_combination


def solve(input):
    with open(input) as file:
        lines = [line.strip() for line in file.readlines()]
        separator_index = lines.index("")
        init_states = lines[:separator_index]
        eqs = lines[separator_index+1:]
    
    return (part1(init_states, eqs), part2(eqs))


if __name__ == "__main__":
    input = "input.txt"
    result = solve(input)
    print("Part 1:", result[0])
    print("Part 2:", result[1])