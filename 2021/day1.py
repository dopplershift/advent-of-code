def run(data):
    return solve(data), solve(data, apart=3)


def solve(s, apart=1):
    vals = list(map(int, s.split('\n')))
    # Running windows have all items in common except first/last
    # so instead of comparing sums of windows, compare differing items
    return sum(b > a for a, b in zip(vals[:-apart], vals[apart:]))


if __name__ == '__main__':
    from aocd.models import Puzzle

    sample = '''199
200
208
210
200
207
240
269
260
263'''

    test_a, test_b = run(sample)
    assert test_a == 7
    assert test_b == 5

    puz = Puzzle(2021, 1)
    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
