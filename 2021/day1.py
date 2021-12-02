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

    assert solve(sample) == 7
    assert solve(sample, apart=3) == 5

    puz = Puzzle(2021, 1)

    puz.answer_a = solve(puz.input_data)
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = solve(puz.input_data, apart=3)
    print(f'Part 2: {puz.answer_b}')