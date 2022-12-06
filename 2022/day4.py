def parse(l):
    rng1, rng2 = l.split(',')
    return tuple(map(int, rng1.split('-'))), tuple(map(int, rng2.split('-')))


def fully_contained(*ranges):
    r1, r2 = sorted(ranges, key=lambda r: (r[0], r[0] - r[1]))
    return r1[0] <= r2[0] and r1[1] >= r2[1]


def overlaps(*ranges):
    r1, r2 = sorted(ranges, key=lambda r: (r[0], r[0] - r[1]))
    return not r2[0] > r1[1]


def run(data):
    ranges = [parse(l) for l in data.split('\n')]
    return sum(fully_contained(*r) for r in ranges), sum(overlaps(*r) for r in ranges)


if __name__ == '__main__':
    from aocd.models import Puzzle

    sample = '''2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8'''

    test_a, test_b = run(sample)
    assert test_a == 2
    assert test_b == 4

    puz = Puzzle(2022, 4)
    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
