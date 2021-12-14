def run(data):
    vals = list(map(int, data.split('\n')))
    return sum(i // 3 - 2 for i in vals), sum(total_fuel(i) for i in vals)


def total_fuel(mass):
    total = 0
    while mass:
        mass = max(mass // 3 - 2, 0)
        total += mass
    return total


if __name__ == '__main__':
    from aocd.models import Puzzle

    sample = '''14
1969
100756'''

    test_a, test_b = run(sample)
    assert test_a == 34239
    assert test_b == 51314

    puz = Puzzle(2019, 1)
    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
